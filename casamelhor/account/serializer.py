from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet


class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    user_permissions = serializers.ListField(write_only=True, required=False)
    groups = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = "__all__"
        extra_fields = ['permissions', 'groups']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        permissions = None
        groups = None
        if 'user_permissions' in validated_data and validated_data['user_permissions']:
            permissions = validated_data['user_permissions']
        if 'groups' in validated_data and validated_data['groups']:
            groups = validated_data['groups']
        validated_data.pop('groups')
        validated_data.pop('user_permissions')
        obj = super(AuthUserSerializer, self).create(validated_data)
        if permissions:
            obj.user_permissions.set(permissions)
        if groups:
            obj.groups.set(groups)
        return obj


class AuthUserPermissionsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    codename = serializers.SerializerMethodField(read_only=True)
    content_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Permission
        fields = "__all__"

    def get_name(self, obj):
        return obj.first().name if isinstance(obj, QuerySet) else obj.name

    def get_codename(self, obj):
        return obj.first().codename if isinstance(obj, QuerySet) else obj.codename

    def get_content_type(self, obj):
        return obj.first().content_type.app_label if isinstance(obj, QuerySet) else obj.content_type.app_label


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
