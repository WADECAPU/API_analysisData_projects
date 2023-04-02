from django.conf import settings

from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.backends import TokenBackend

def get_valid_token_data(request):
    '''Funcion para hacer la obtencion y verificacion de los tokens'''
    token = request.META.get('HTTP_AUTHORIZATION')[7:]
    tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    valid_data = tokenBackend.decode(token, verify=False)
    return valid_data


def validate_token_owner(request, kwargs):
    '''Funcion pata validar el token del usuario o propietario con la ayuda la funcion de arriba '''
    valid_data = get_valid_token_data(request)

    if valid_data['user_id'] != kwargs['owner']:
        stringResponse = {'detail': 'Unauthorized Request'}
        return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
    # Si el token es válido y si el usuario es el propietario, se devuelve una respuesta HTTP de OK
    return Response({'detail': 'Token is valid.'}, status=status.HTTP_200_OK)
