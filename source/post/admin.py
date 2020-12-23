from django.contrib import admin

# Register your models here.
from post.models import Post


class Postadmin(admin.ModelAdmin):
    list_display = ('title',"author","status","slug","category")
    list_filter = ('status','author')
    search_fields = ('status','author__user__username')
    list_display_links = ('title',)
    # def save_model(self, request, obj, form, change):
    #     obj.author=request.user.author
    #     obj.save()

admin.site.register(Post,Postadmin)