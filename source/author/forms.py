from  django import forms
from django.contrib.auth import login, authenticate

from django.utils.translation import ugettext_lazy  as _
from django.contrib.auth.models import User


#
# class UserRegisterForm(forms.Form):
#     user_name=forms.CharField(label=_("user_name"),max_length=150,required=True)
#     password=forms.CharField(label=_('password'),widget=forms.PasswordInput,required=True)
#     password_confirm = forms.CharField(label=_('password'), widget=forms.PasswordInput, required=True)
#     email=forms.EmailField(label=_("email"))
#     avatar=forms.ImageField(label=_("avatar"))
#     first_name=forms.CharField(label=_("first_name"))
#
#
# class UserLogin(forms.Form):
#     user_name = forms.CharField(label=_("user_name"), max_length=150, required=True)
#     password = forms.CharField(label=_('password'), widget=forms.PasswordInput, required=True)
#
# # class AuthorForm(ModelForm):
# #     class Meta:
# #         model = User
# #         fields = ['name', 'title', 'birth_date']
#
#
#
# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
#
#
# class EmployerForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username','password',)



class LoginForm(forms.Form):
    username=forms.CharField(max_length=150)
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user=User.objects.filter(username=self.cleaned_data['username']).first()
        if user is None:
            raise forms.ValidationError(_("user with this username does not extists"))

        user=authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError(_("Unable to login with provided credentials"))
        self.cleaned_data['user']=user
        return self.cleaned_data


class RegistrationFrom(forms.Form):
    email=forms.EmailField()
    username = forms.CharField(label=_('username'),max_length=150)
    password = forms.CharField(label=_('password'),widget=forms.PasswordInput)
    password_2=forms.CharField(widget=forms.PasswordInput)


    def clean(self):
        password = self.cleaned_data.get('password', None)
        password_2 = self.cleaned_data.get('password_2', None)
        if password != password_2:
            raise forms.ValidationError(_("password don't match"), code='invalid')
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(_("username already exists"))
        if User.objects.filter(username=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_("email already exists"))
    def save(self):
        data={
            'email':self.cleaned_data.get('email'),
            'password':self.cleaned_data.get('password'),
            'username':self.cleaned_data.get('username')

        }
        user=User.objects.create_user(username=data['username'],password=data['password'],email=data['email'])

        return user

