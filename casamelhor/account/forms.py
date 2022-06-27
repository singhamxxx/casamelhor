from django import forms
from .models import User, Role
from django.contrib.auth.models import Group, Permission
from django.db.models import Q


class AdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = '__all__'


class RegisterForm(forms.ModelForm):
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all())
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    image = forms.ImageField(required=False)
    password = forms.CharField(required=True)
    is_email = forms.BooleanField(required=False)
    is_phone = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('phone', 'email', 'password', 'first_name', 'role', 'image', 'is_email', 'is_phone', 'user_permissions', 'groups')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if "email" in cleaned_data:
            if User.objects.filter(email=cleaned_data['email']).exists():
                raise forms.ValidationError("Email Already Exists !!!")
        if "phone" in cleaned_data:
            if User.objects.filter(phone=cleaned_data['phone']).exists():
                raise forms.ValidationError("phone Already Exists !!!")
        return cleaned_data


class UserLoginForm(forms.Form):
    phone_or_email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['phone_or_email', 'password']

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        if "phone_or_email" in cleaned_data:
            u_e = cleaned_data['phone_or_email']
            if not User.objects.filter(Q(email=u_e) | Q(phone=u_e)).exists():
                raise forms.ValidationError("User is not Exists!!!")
        return cleaned_data


class UserEmailVerificationForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    otp = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'otp']

    def clean(self):
        cleaned_data = super(UserEmailVerificationForm, self).clean()
        if not User.objects.filter(email=cleaned_data['email']).exists():
            raise forms.ValidationError("User is not Exists!!!")
        return cleaned_data


class AuthUserGroupOFPermissionsForm(forms.Form):
    name = forms.CharField(required=True)
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=True)

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def clean(self):
        cleaned_data = super(AuthUserGroupOFPermissionsForm, self).clean()
        if Group.objects.filter(name=cleaned_data['name']).exists():
            raise forms.ValidationError("User permission`s group is already Exists!!!")
        return cleaned_data
