from rest_framework import serializers
from .models import User, Vault, Role, Company
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet


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
    permissions = AuthUserPermissionsSerializer(many=True, read_only=True)
    permission_ids = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"

    def get_name(self, obj):
        return obj.first().name if isinstance(obj, QuerySet) else obj.name

    def get_permission_ids(self, obj):
        return [i.id for i in obj.permissions.all()]


class RoleSerializer(serializers.ModelSerializer):
    group = AuthUserGroupOFPermissionsSerializer(many=False)

    class Meta:
        model = Role
        fields = ('id', 'role', 'group')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    user_permissions = AuthUserPermissionsSerializer(many=True, read_only=True)
    groups = AuthUserGroupOFPermissionsSerializer(many=True, read_only=True)
    role = RoleSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True},
                        'role_id': {'source': 'role', 'write_only': True}, 'company_id': {'source': 'company', 'write_only': True}}
        fields = ["id", "email", "phone", "first_name", "last_name", "role", "is_superuser", "is_staff", "is_active", "date_joined", "employee_id",
                  "department", "is_email", "is_phone", "updated_at", "user_permissions", "groups", "role_id", "password", 'image', 'company',
                  'user_permissions', 'groups', 'role_id', 'company_id']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        permissions = None
        groups = None
        if 'user_permissions' in validated_data and validated_data['user_permissions']:
            permissions = validated_data['user_permissions']
            validated_data.pop('user_permissions')
        if 'groups' in validated_data and validated_data['groups']:
            groups = validated_data['groups']
            validated_data.pop('groups')
        obj = super(AuthUserSerializer, self).create(validated_data)
        if permissions:
            obj.user_permissions.set(permissions)
        if groups:
            obj.groups.set(groups)
        return obj


class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = "__all__"


class AuthUserSimpleDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'role', 'employee_id', 'department', 'phone', 'image', 'is_email', 'is_phone', 'is_active', 'is_staff', 'is_superuser']
