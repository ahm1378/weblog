from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


from author.forms import SignUpForm



#with AuthenticationForm
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'weblog/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# def login_view_forms(request):
#     if request.user.is_authenticated:
#         return redirect('posts_archive')
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         user = authenticate(request, username=username, password=password)
#         if user and user.is_active:
#             login(request, user)
#             return redirect('posts_archive')
#     else:
#         pass
#     return render(request, 'blog/login.html', context={})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('weblog/home.html')
    else:
        form = SignUpForm()
    return render(request, 'weblog/register.html', {'form': form})