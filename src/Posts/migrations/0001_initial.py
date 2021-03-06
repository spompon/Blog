# Generated by Django 3.0.6 on 2020-09-24 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Titre')),
                ('slug', models.SlugField(unique=True)),
                ('body', models.TextField(verbose_name='Contenu')),
                ('picture', models.ImageField(upload_to='posts', verbose_name='Image')),
                ('alt_picture', models.CharField(default='description', max_length=50, verbose_name='Description Image')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('featured', models.BooleanField(default=False, verbose_name='En vedette')),
                ('star', models.BooleanField(default=False, verbose_name='Article Star')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Auteur')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='Posts.Category', verbose_name='Catégorie')),
                ('tags', models.ManyToManyField(blank=True, to='Posts.Tag')),
            ],
            options={
                'ordering': ['-published_date'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_posts', models.ManyToManyField(to='Posts.Post')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Membre')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titre')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('body', models.TextField(max_length=100, null=True, verbose_name='Contenu')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False, verbose_name='Approuvé')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Posts.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
    ]
