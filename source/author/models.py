from django.db import models

# Create your models here.
from  django.contrib.auth import get_user_model
from lib.models import BaseModel
from  django.contrib.auth.models import AbstractUser



User=get_user_model()


# class MyUser(AbstractUser):
#     email = models.EmailField(_('email address'), unique=True,db_index=True)
#     full_name=models.CharField()
#     EMAIL_FIELD = "email"
#     USERNAME_FIELD =  "email"
#     REQUIRED_FIELDS = ['email','fullname']
#     def clean(self):
#         self.email=self.__class__.objects.normalize_email(self.email)
#
#     def get_full_name(self):
#         return self.full_name



class Author(BaseModel):
    avatar=models.ImageField(verbose_name="avatar",upload_to="author/avatars/")
    user =models.OneToOneField(User,related_name="author",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name="Author"
        verbose_name_plural="Authors"
        db_table = "author"