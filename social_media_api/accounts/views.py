from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer,ProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class TokenView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
            return Response({'token': token.key})
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if request.user.is_authenticated:
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data)
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    




