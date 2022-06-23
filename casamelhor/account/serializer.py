from rest_framework import serializers
from .models import User, Permission, Group
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet


class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = "__all__"

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(AuthUserSerializer, self).create(validated_data)


class AuthUserPermissionsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    codename = serializers.SerializerMethodField(read_only=True)
    content_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Permission
        fields = "__all__"

    def get_name(self, obj):
        return obj.first().name

    def get_codename(self, obj):
        return obj.first().codename

    def get_content_type(self, obj):
        return obj.first().content_type.app_label


class AuthUserGroupOFPermissionsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"

    def get_name(self, obj):
        return obj.first().name if isinstance(obj, QuerySet) else obj.name

    def get_permissions(self, obj):
        return list(obj.first().permissions.all().values('id', 'name')) if isinstance(obj, QuerySet) else list(obj.permissions.all().values('id', 'name'))
