from django.db import models

# Create your models here.
from lib.models import BaseModel


class Category(BaseModel):
    title = models.CharField(verbose_name="Title", max_length=50)
    slug = models.SlugField(verbose_name="slug", unique=True, db_index=True)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children', related_query_name='children')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.slug