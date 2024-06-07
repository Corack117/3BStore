from rest_framework import serializers

from .models import User

class UserAuthenticateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password"
        ]
        read_only_fields = fields

class UserSerializer(serializers.ModelSerializer):
    slug = serializers.UUIDField(read_only=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'slug',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'last_login'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance: User, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)