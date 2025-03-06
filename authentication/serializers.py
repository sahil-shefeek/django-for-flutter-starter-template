from dj_rest_auth.app_settings import api_settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import InterfaceUser


class InterfaceUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="interfaceuser-detail")
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = InterfaceUser
        fields = ["url", "id", "name", "email", "is_admin", "avatar"]

    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class InterfaceUserCreateSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="interfaceuser-detail")

    class Meta:
        model = InterfaceUser
        fields = ["url", "id", "name", "email", "username", "password", "avatar"]
        read_only_fields = ["id"]

    def __init__(self, *args, **kwargs):
        self.user_type = kwargs.pop("user_type", None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        name = validated_data["name"]
        email = validated_data["email"]
        username = validated_data.get("username")
        password = validated_data["password"]
        if self.user_type == "admin":
            user = InterfaceUser.objects.create_admin(email, name, password)
        elif self.user_type == "user":
            user = InterfaceUser.objects.create_user(email, name, password)
        else:
            raise serializers.ValidationError("Invalid user type.")
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        # Get avatar URL if it exists
        avatar_url = None
        if user.avatar:
            request = self.context.get("request")
            if request:
                avatar_url = request.build_absolute_uri(user.avatar.url)
            else:
                avatar_url = user.avatar.url
                
        data.update(
            {
                "user": {
                    "name": user.name,
                    "email": user.email,
                    "username": user.username,
                    "is_admin": user.is_admin,
                    "avatar": avatar_url,
                }
            }
        )
        return data


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = InterfaceUser
        fields = ("email", "name", "username", "is_admin", "avatar")
        read_only_fields = ("email", "is_admin")

    def get_avatar(self, obj):
        """
        Returns only the absolute URL for the avatar image suitable for frontend use.
        """
        if obj.avatar:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class CustomJWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication without refresh token in response body.
    """

    access = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER from settings
        """
        UserDetailsSerializer = api_settings.USER_DETAILS_SERIALIZER
        user_data = UserDetailsSerializer(obj["user"], context=self.context).data
        return user_data
