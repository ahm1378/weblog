from django.db import models

# Create your models here.
from author.models import Author
# from category.models import Category
# Create your models here.
from category.models import Category
from lib.models import BaseModel


class Post(BaseModel):
    STATUS_CHOICES = (
        (0, 'DRAFT'),
        (1, 'PUBLISHED'),
        (2, 'ARCHIVED')
    )
    status = models.PositiveSmallIntegerField(verbose_name="status", choices=STATUS_CHOICES,
                                              default=0)
    title = models.CharField(verbose_name="title", max_length=100)
    slug = models.SlugField(verbose_name="Slug", db_index=True, unique=True)
    body = models.TextField(verbose_name="body")
    author = models.ForeignKey(Author, related_name="Posts", on_delete=models.SET_DEFAULT, default=1)
    attachment = models.FileField(
        verbose_name="attachment", upload_to="post/attachments/", null=True)
    category = models.ForeignKey(Category, verbose_name="category", on_delete=models.CASCADE)
    create_at = models.DateTimeField(verbose_name="Create at", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Update at", auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        db_table = "post"

    def __str__(self):
        return self.title