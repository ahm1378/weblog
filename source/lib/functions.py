from category.models import Category


def get_category():
    return  Category.objects.all()