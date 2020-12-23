from django.contrib import admin

# Register your models here.
from category.models import Category

class ChildrenItemInline(admin.TabularInline):
    model = Category
    fields = (
        'title', 'slug'
    )
    extra = 1
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent')
    search_fields = ('slug', 'title')
    list_filter = ('parent',)
    inlines = [
        ChildrenItemInline,
    ]
admin.site.register(Category,CategoryAdmin)