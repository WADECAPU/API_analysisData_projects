#from django.conf import settings

from rest_framework import  status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#from rest_framework_simplejwt.backends import TokenBackend

from authApp.utils import get_valid_token_data, validate_token_owner
from authApp.models import New
from authApp.serializers import NewSerializer
from authApp.permissions import IsOwner


class NewsCreateView(generics.CreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        valid_data = get_valid_token_data(request)

        if valid_data['user_id'] != request.data['owner']:
            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = NewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Noticia creada', status=status.HTTP_201_CREATED)
    

class NewsListView(generics.ListAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer


class NewsDetailView(generics.RetrieveAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class NewsUpdateView(generics.UpdateAPIView):
    '''Esta vista valida el token y si hay algún error retorna una respuesta de error,
      en caso contrario llama a la función get, put o delete de la clase padre y devuelve su resultado''' 
    
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def put(self, request, *args, **kwargs):
        verificacion = validate_token_owner(request, kwargs)
        if verificacion:#si hay algún error, se devuelve una respuesta de error y si es lo contrario sigue con el proceso
            return verificacion
        
        return super().put(request, *args, **kwargs)
    
    
class NewsDeleteView(generics.DestroyAPIView):
    '''Esta vista valida el token y si hay algún error retorna una respuesta de error,
      en caso contrario llama a la función get, put o delete de la clase padre y devuelve su resultado'''
     
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def delete(self, request, *args, **kwargs):
        verificaacion = validate_token_owner(request, kwargs)
        if verificaacion:#si hay algún error, se devuelve una respuesta de error y si es lo contrario sigue con el proceso
            return verificaacion
        return super().destroy(request, *args, **kwargs)
