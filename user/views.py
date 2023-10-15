from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """API view for user registration."""

    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API view for viewing and updating user profile."""

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> get_user_model():
        """Retrieve the current authenticated user."""
        return self.request.user
