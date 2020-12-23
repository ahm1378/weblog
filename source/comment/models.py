from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from author.models import Author
from lib.models import BaseModel
from post.models import Post


class CommentLike(BaseModel):
    author = models.ForeignKey(Author, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', verbose_name=_(
        'Comment'),  related_name='comment_like', related_query_name='comment_like', on_delete=models.CASCADE)
    condition = models.BooleanField(_("Condition"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        unique_together = [['author', 'comment']]
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return str(self.condition)


class Comment(BaseModel):
    content = models.TextField(_("Content"))
    post = models.ForeignKey(Post, verbose_name=_(
        "Post"), on_delete=models.CASCADE)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    author = models.ForeignKey(Author, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(_("confirm"), default=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-create_at']

    def __str__(self):
        return self.post.title

    @property
    def like_count(self):
        q = CommentLike.objects.filter(comment=self, condition=True)
        return q.count()

    @property
    def dislike_count(self):
        q = self.comment_like.filter(condition=False)
        return q.count()
