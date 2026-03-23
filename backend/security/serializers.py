from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['roles'] = list(user.groups.values_list('name', flat=True))
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'roles': list(self.user.groups.values_list('name', flat=True))
        }
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    contact_no = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'contact_no']

    def create(self, validated_data):
        contact_no = validated_data.pop('contact_no', None)
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        
        customer_group = Group.objects.get(name='Customer')
        user.groups.add(customer_group)
        
        if contact_no:
            from api.UserProfile.model import UserProfile
            UserProfile.objects.create(user=user, contact_no=contact_no)
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)