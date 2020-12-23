from  django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy  as _
from django.contrib.auth.models import User
from author.models import Author
from  comment.models import  Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        labels=('content',_("comment"))
        widgets = {
            'content': forms.Textarea,
        }
