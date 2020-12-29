import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from author.models import Author
from comment.models import Comment, CommentLike


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