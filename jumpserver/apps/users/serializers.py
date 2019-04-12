from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True, label="密码", help_text="密码")
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="上次登录时间")

    class Meta:
        model = User
        fields = ("id", "username", "password", "name", "email", "is_superuser",
                  "is_active", "last_login", "remark")

    def create(self, validated_data):
        password = validated_data["password"]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()
        return instance


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
