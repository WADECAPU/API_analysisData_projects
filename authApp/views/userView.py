from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authApp.utils import get_valid_token_data, validate_token_owner
from authApp.models import User
from authApp.serializers import UserSerializer


class UserCreateView(views.APIView):
    '''Vista para la creacion de usuarios'''
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tokenData = {
            'email':request.data['email'],
            'password': request.data['password']
        }
        tokenSerializer = TokenObtainPairSerializer(data=tokenData)
        tokenSerializer.is_valid(raise_exception=True)

        return Response(tokenSerializer.validated_data, status=status.HTTP_201_CREATED)
    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    '''Esta vista primero valida el token y si hay algún error retorna una respuesta de error,
      en caso contrario llama a la función get, put o delete de la clase padre y devuelve su resultado'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        verificacion = validate_token_owner(request, kwargs)
        if verificacion:#si hay algún error, se devuelve una respuesta de error y si es lo contrario sigue con el proceso
            return verificacion
        
        return super().get(request, *args, **kwargs)
