from django.contrib import admin

# Register your models here.
from author.models import Author

class AuthorAddmin(admin.ModelAdmin):
    list_display = ('user__username','user__password','usser__firstname')
    list_filter = ('user__name',)



admin.site.register(Author)