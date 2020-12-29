from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic.base import View

from author.forms import RegistrationFrom, LoginForm
from weblog import settings


class RegisretView(FormView):

    form_class = RegistrationFrom
    template_name = "user/register.html"
    success_url = '/home/'

    def form_valid(self, form):
        form.save()
        return  super().form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = '/home/'

    def form_valid(self, form):
        login(self.request,form.cleaned_data['user'])
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/home/')