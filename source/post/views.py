from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, FormView, DetailView
# Create your views here.
from author.forms import LoginForm, RegistrationFrom
from category.models import Category
from lib.functions import get_category
from post.models import Post


def post_list(request):
    posts = Post.objects.all()
    title = posts.values_list('title', flat=True)
    return HttpResponse("post-page count: {} <br> titles :{}".format(posts.count(), ' '.join(title)))


def home(request):
    post_count = Post.objects.all().count()
    post_list=Post.objects.all()[2:post_count]


    user=request.user.id
    category_list=Category.objects.all()

    context={'post_count':post_count,
             "post_titles":post_list,"category_list":category_list}

    return render(request,"weblog/home.html",context)


def post_details(request,slug):
    post=Post.objects.filter(slug=slug).first()
    context={"post":post,"category_list":get_category()}
    return render(request,'weblog/postSingle.html',context=context)


def get_post_username(request,id):

    post_user=Post.objects.filter(author__id=id)
    context = {"post_user": post_user, "category_list": get_category()}

    return render(request, 'weblog/userpost.html', context=context)

def get_post_category(request,id):

    post_cat=Post.objects.filter(category__id=id)
    context = {"post_cat": post_cat, "category_list": get_category()}

    return render(request, 'weblog/categorypost.html', context=context)


#classbaseview
class PostArchive(ListView):
    post_count = Post.objects.all().count()
    model = Post

    queryset = Post.objects.all()[2:post_count]
    template_name = 'weblog/home.html'


def get_context_data(self, *, object_list=None, **kwargs):
    """Get the context for this view."""
    queryset = object_list if object_list is not None else self.object_list
    page_size = self.get_paginate_by(queryset)
    context_object_name = self.get_context_object_name(queryset)
    if page_size:
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
        context = {
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            'object_list': queryset
        }
    else:
        context = {
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
            'object_list': queryset
        }
    if context_object_name is not None:
        context[context_object_name] = queryset
    context.update(kwargs)
    return super().get_context_data(**context)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'weblog/login.html'
    success_url = '/home/'

    def form_valid(self, form):
        user=authenticate()
        return super().form_valid(form)




class RegisretView(FormView):

    form_class = RegistrationFrom
    template_name = "weblog/register.html"
    success_url = '/home/'

    def form_valid(self, form):
        form.save()
        return  super().form_valid(form)




class PostSingle(DetailView):
    model = Post
    template_name = 'weblog/postSingle.html'


class CategorySingle(DetailView):
    pass