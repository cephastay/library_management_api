from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.contrib.auth import get_user_model

from accounts.serializers import RegisterSerializer, UserProfileSerializer, PasswordSerializer
from utils.custom_permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin, HasAccountOrNone

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing user objects, including user registration,
    profile updates, and password changes.
    """
    serializer_class = RegisterSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Adjust permissions dynamically based on the action being performed.
        """
        if self.action == 'create':
            self.permission_classes = [HasAccountOrNone]
        elif self.action in ['destroy', 'update', 'partial_update', 'change_password']:
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        """
        Use different serializers based on the action being performed.
        """
        if self.action in ['update', 'partial_update']:
            return UserProfileSerializer
        return super().get_serializer_class(*args, **kwargs)

    @action(
        detail=True,
        methods=['get', 'post'],
        serializer_class=PasswordSerializer,
        permission_classes=[IsOwnerOrAdmin],
    )
    def change_password(self, request, pk=None, format=None):
        """
        Custom action to allow users to change their password.
        Supports both GET (to retrieve user data) and POST (to update the password).
        """
        user = self.get_object()

        if request.method == 'POST':
            serializer = self.serializer_class(user, data=request.data, partial=False)

            if serializer.is_valid(raise_exception=True):
                old_password = serializer.validated_data.get('old_password')
                new_password = serializer.validated_data.get('new_password')
                confirm_password = serializer.validated_data.get('confirm_password')

                if new_password != confirm_password:
                    return Response({"detail": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

                if not user.check_password(old_password):
                    return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response({"detail": "Password updated successfully."}, status=status.HTTP_202_ACCEPTED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
