from django import forms
from .models import User, Role, document_choices, Vault, Company
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
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    password = forms.CharField(required=True)
    is_email = forms.BooleanField(required=False)
    is_phone = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('phone', 'email', 'password', 'first_name', 'role', 'is_email', 'is_phone', 'company', 'user_permissions', 'groups')

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


class AuthUserGroupOFPermissionsForm(forms.ModelForm):
    name = forms.CharField(required=True)
    group = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=True)

    class Meta:
        model = Group
        fields = ['name', 'group']

    def clean(self):
        cleaned_data = super(AuthUserGroupOFPermissionsForm, self).clean()
        return cleaned_data


class AuthUserProfileForm(forms.ModelForm):
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)
    first_name = forms.CharField(required=True)
    employee_id = forms.CharField(required=True)
    department = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['phone', 'email', 'image', 'first_name', 'employee_id', 'department']

    def clean(self):
        cleaned_data = super(AuthUserProfileForm, self).clean()
        return cleaned_data


class VaultForm(forms.ModelForm):
    is_indian = forms.BooleanField(required=True)
    type = forms.ChoiceField(choices=document_choices, required=False)
    document = forms.ImageField(required=False)
    passport_photo = forms.ImageField(required=False)
    visa_photo = forms.ImageField(required=False)
    address1 = forms.CharField(widget=forms.TextInput(), required=False)
    address2 = forms.CharField(widget=forms.TextInput(), required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)
    passport_number = forms.CharField(required=False)
    passport_country_of_issued = forms.CharField(required=False)
    passport_date_of_issued = forms.DateField(input_formats="%Y-%m-%d", required=False)
    passport_expire_date = forms.DateField(input_formats="%Y-%m-%d", required=False)
    visa_issued_date = forms.DateField(input_formats="%Y-%m-%d", required=False)
    visa_expire_date = forms.DateField(input_formats="%Y-%m-%d", required=False)

    class Meta:
        model = Vault
        fields = ['is_indian', 'type', 'document', 'passport_photo', 'visa_photo', 'address1', 'address2', 'city',
                  'country', 'zip_code', 'passport_number', 'passport_country_of_issued', 'passport_date_of_issued',
                  'passport_expire_date', 'visa_issued_date', 'visa_expire_date']

    def clean(self):
        cleaned_data = super(VaultForm, self).clean()
        return cleaned_data
