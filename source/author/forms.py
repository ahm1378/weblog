from  django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy  as _
from django.contrib.auth.models import User
from author.models import Author


class UserRegisterForm(forms.Form):
    user_name=forms.CharField(label=_("user_name"),max_length=150,required=True)
    password=forms.CharField(label=_('password'),widget=forms.PasswordInput,required=True)
    password_confirm = forms.CharField(label=_('password'), widget=forms.PasswordInput, required=True)
    email=forms.EmailField(label=_("email"))
    avatar=forms.ImageField(label=_("avatar"))
    first_name=forms.CharField(label=_("first_name"))


class UserLogin(forms.Form):
    user_name = forms.CharField(label=_("user_name"), max_length=150, required=True)
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput, required=True)

# class AuthorForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'title', 'birth_date']



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EmployerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password',)



class LoginForm(forms.Form):
    username=forms.CharField(max_length=150)
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user=User.objects.filter(username=self.cleaned_data['username']).first()
        if user is None:
            raise forms.ValidationError(_("user with this username does not extists"))
        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError(_("wrong password"))
        return self.cleaned_data


class RegistrationFrom(forms.Form):
    email=forms.EmailField()
    username = forms.CharField(label=_('username'),max_length=150)
    password = forms.CharField(label=_('password'),widget=forms.PasswordInput)
    password_2=forms.CharField(widget=forms.PasswordInput)


    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        if password != password2:
            raise forms.ValidationError(_("password don't match"), code='invalid')
        if User.objects.filter(username=self.cleaned_data['username']).exixts():
            raise forms.ValidationError(_("username already exists"))
        if User.objects.filter(username=self.cleaned_data['email']).exixts():
            raise forms.ValidationError(_("email already exists"))
    def save(self):
        user=User.objects.create_user(**self.cleaned_data)
        return user

