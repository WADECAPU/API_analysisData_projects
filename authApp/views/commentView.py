from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authApp.models import Comment
from authApp.serializers import CommentSerializer
from authApp.permissions import IsOwner
from authApp.utils import get_valid_token_data, validate_token_owner


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        valid_data = get_valid_token_data(request)

        if valid_data['user_id'] != request.data['owner']:
            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Comentario realizado', status=status.HTTP_201_CREATED)
    

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentUpdateView(generics.UpdateAPIView):
    '''Esta vista valida el token y si hay algún error retorna una respuesta de error,
      en caso contrario llama a la función get, put o delete de la clase padre y devuelve su resultado'''
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def put(self, request, *args, **kwargs):
        verificacion = validate_token_owner(request, kwargs)
        if verificacion:#si hay algún error, se devuelve una respuesta de error y si es lo contrario sigue con el proceso
            return verificacion

        return super().put(request, *args, **kwargs)


class CommentDeleteView(generics.DestroyAPIView):
    '''Esta vista valida el token y si hay algún error retorna una respuesta de error,
      en caso contrario llama a la función get, put o delete de la clase padre y devuelve su resultado''' 
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def delete(self, request, *args, **kwargs):
        verificacion = validate_token_owner(request, kwargs)
        if verificacion:#si hay algún error, se devuelve una respuesta de error y si es lo contrario sigue con el proceso
            return verificacion
        
        return super().destroy(request, *args, **kwargs)