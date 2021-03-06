# Generated by Django 3.1.4 on 2020-12-03 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'DRAFT'), (1, 'PUBLISHED'), (2, 'ARCHIVED')], default=0, verbose_name='status')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('body', models.TextField(verbose_name='body')),
                ('attachment', models.FileField(null=True, upload_to='post/attachments/', verbose_name='attachment')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update at')),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Posts', to='author.author')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'db_table': 'post',
            },
        ),
    ]
