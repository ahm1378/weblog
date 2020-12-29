"""weblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('weblog/', include('weblog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from author.views import RegisretView, LoginView
from comment.views import like_comment, create_comment
from post.views import post_list, home, post_details, get_post_username, get_post_category, PostArchive, PostSingle

urlpatterns = [
    path('admin/', admin.site.urls),

    path('home/',PostArchive.as_view(),name='home'),
    path('home/post/<slug:slug>',post_details,name="post_detail"),
    path('register/',RegisretView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('home/user<int:id>/',get_post_username,name="Get_post_username"),
    path('home/category<int:id>/', get_post_category, name="getcategory"),
    path('home/like_comment/', like_comment, name='like_comment'),
    path('home/comments/', create_comment, name='add_comment'),

    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)