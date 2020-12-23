from django.shortcuts import render

# Create your views here.
from category.models import Category
from lib.functions import get_category


def category_list(request):
    category_list = get_category()
    content={"category_list":category_list}
    return render(request, "weblog/base.html", context=content)