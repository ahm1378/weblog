import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, DetailView
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




class LoginView(FormView):
    form_class = LoginForm
    template_name = 'weblog/login.html'
    success_url = '/home/'

    def form_valid(self, form):
        login(self.request,form.cleaned_data['user'])
        return super().form_valid(form)




class RegisretView(FormView):

    form_class = RegistrationFrom
    template_name = "weblog/register.html"
    success_url = '/home/'

    def form_valid(self, form):
        form.save()
        return  super().form_valid(form)

@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    author_mine=Author.objects.filter(user=user).first()
    try:
        comment = Comment.objects.create(post_id=data['post_id'], content=data['content'], author=author_mine)
        response = {"comment_id": comment.id, "content": comment.content, 'dislike_count': 0, 'like_count': 0,
                    'full_name': user.get_full_name()}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {"error": 'error'}
        return HttpResponse(json.dumps(response), status=400)


class PostSingle(DetailView):
    model = Post
    template_name = 'weblog/postSingle.html'



@csrf_exempt
@login_required
def like_comment(request):
    data = json.loads(request.body)
    print(request.body)
    user = request.user
    author_mine=Author.objects.filter(user=user).first()
    print(type(author_mine))
    try:
        comment = Comment.objects.get(id=data['comment_id'])
        print(comment)
    except Comment.DoesNotExist:
        return HttpResponse('bad request', status=404)
    try:
         comment_like = CommentLike.objects.get(author=author_mine, comment=comment)
         comment_like.condition = data['condition']
         comment_like.save()
    except CommentLike.DoesNotExist:
        CommentLike.objects.create(author=author_mine, condition=data['condition'], comment=comment)
    response = {"like_count": comment.like_count, 'dislike_count': comment.dislike_count}
    return HttpResponse(json.dumps(response), status=201)