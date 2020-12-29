from django.contrib.auth import login
from django.views.generic import FormView

from author.forms import RegistrationFrom, LoginForm


class RegisretView(FormView):

    form_class = RegistrationFrom
    template_name = "weblog/register.html"
    success_url = '/home/'

    def form_valid(self, form):
        form.save()
        return  super().form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'weblog/login.html'
    success_url = '/home/'

    def form_valid(self, form):
        login(self.request,form.cleaned_data['user'])
        return super().form_valid(form)