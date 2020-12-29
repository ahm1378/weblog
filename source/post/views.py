import json
from urllib.request import Request

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, DetailView, CreateView
# Create your views here.
from author.forms import LoginForm, RegistrationFrom
from author.models import Author
from category.models import Category
from comment.commentform import CommentForm
from comment.models import Comment, CommentLike
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
    user=request.user
    post=Post.objects.filter(slug=slug).first()
    context={"post":post,
             "category_list":get_category(),
             'form': CommentForm(),
             'comments': post.comment_set.filter(is_confirmed=True)}
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=Author.objects.filter(user=user).first()
            comment.post = post
            comment.save()
        else:
            context['form'] = form

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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = get_category()
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    def form_valid(self, form):
        post = get_object_or_404(Request, slug = self.kwargs ['slug'])
        user=request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=Author.objects.filter(user=user).first()
            comment.post = post
            comment.save()
        return super().form_valid(form)


class CategoryDetails(DetailView):
    model = Category
    template_name = 'weblog/categorypost.html'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['post_cat'] =Post.objects.filter(category__id=self.kwargs.get('pk'))
        context['category_list'] = get_category()

        return context






class PostSingle(DetailView):
    model = Post
    template_name = 'weblog/postSingle.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        context['comments'] = post.comment_set.filter(is_confirmed=True)
        context['form'] = CommentForm()
        context['category_list'] = get_category()
        return context



