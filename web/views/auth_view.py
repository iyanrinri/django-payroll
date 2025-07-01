from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from web.serializers.auth_serializer import AuthSerializer
from drf_yasg import openapi

class AuthLogin(generics.CreateAPIView):
    serializer_class = AuthSerializer

    @swagger_auto_schema(
        operation_id="auth_login",
        request_body=AuthSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)