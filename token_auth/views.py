from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status
import json
from django.contrib.auth.models import User

class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class RegisterView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        data = {
            'username': username,
            'password': request.data.get('password')
        }
        print(json.dumps(data))
        if User.objects.filter(username=username).exists():
            return Response({
                'error': f'Unable To Register {username}',
            }, status=status.HTTP_409_CONFLICT)
        
        
        User.objects.create_user(username=username, email=username, password=request.data.get('password'))

        serializer = self.serializer_class(data=json.dumps(data),
                                           context={'request': request})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        