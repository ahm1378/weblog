# Generated by Django 3.1.4 on 2020-12-30 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='author/avatars/', verbose_name='avatar'),
        ),
    ]
