from rest_framework import serializers
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    """
    A serializer for creating user instances in the Library Management API.
    Includes custom validation for email and password fields.
    """
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    ) 
    joined = serializers.DateField(
        source='profile.member_since',
        read_only=True
    )
    status = serializers.CharField(
        source='profile.role',
        read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            'password', 'username', 'email',
            'joined', 'status', 'url', 'bio'
        ]
        extra_kwargs = {
            'url': {
                'view_name': 'users-detail',
                'lookup_field': 'pk'
            },
            'bio': {
                'required': False  
            }
        }

    def validate(self, attrs):
        email_exists = get_user_model().objects.filter(
            email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError({'email': 'User with this email already exists.'})
        return attrs

    def validate_password(self, value):
        """
        Validate the password using Django's built-in password validation.
        Provide detailed error messages for invalid passwords.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return value

    def validate_email(self, value):
        """
        Ensure the email follows a valid format.
        """
        re_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(re_pattern, value):
            raise serializers.ValidationError(f"{value} is not a valid email address.")
        return value

    def create(self, validated_data):
        """
        Create a new user instance, ensuring the password is hashed.
        """
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    A serializer for retrieving user profile details.
    Includes fields for the user's join date and role.
    """
    date_joined = serializers.DateField(source='profile.member_since', read_only=True)
    role = serializers.CharField(source='profile.role', read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'bio', 'date_joined',
            'role'
        ]

class PasswordSerializer(serializers.ModelSerializer):
    """
    A serializer for updating a user's password.
    Validates and securely updates the password.
    """
    old_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Old Password'},
        required=True
    )
    new_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'New Password'},
        required=True
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Confirm New Password'},
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password', 'confirm_password']

    def update(self, instance, validated_data):
        """
        Update the user's password, ensuring it is hashed and saved securely.
        """
        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "New passwords do not match."})

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    def validate_new_password(self, value):
        """
        Validate the password using Django's built-in password validation.
        Provide detailed error messages for invalid passwords.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return value
