from django.db import models
from Accounts.models import User
from django.shortcuts import reverse
from datetime import date


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Auteur')
    title = models.CharField(max_length=100, verbose_name='Titre')
    slug = models.SlugField(max_length=50, unique=True)
    body = models.TextField(verbose_name='Contenu')
    picture = models.ImageField(upload_to='posts', verbose_name='Image',) # On crée un sous-dossier posts dans media_root
    alt_picture = models.CharField(max_length=50, default='description', verbose_name='Description Image')
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', related_name='posts', on_delete=models.CASCADE, verbose_name='Catégorie')
    tags = models.ManyToManyField('Tag', blank=True)
    # comments = models.ForeignKey('Comment', related_name='posts', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Commentaires')
    featured = models.BooleanField(default=False, verbose_name='En vedette')
    star = models.BooleanField(default=False, verbose_name='Article Star')
    #chapeau
    #status

    def __str__(self):
        return self.title.capitalize()

    def cliff(self):
        return self.title[:50]

    # Détails du post
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={
            'slug': self.slug
        })

    # Liste des articles de la catégorie
    def get_category_items(self):
        return reverse('category-list', kwargs={
            'category': self.category
        })

    class Meta:
        ordering = ['-published_date'] # Article les plus récents d'abord


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nom de la catégorie')

    def __str__(self):
        return self.name

    def get_category_list(self):
        return reverse('category-list', kwargs={
            'category': self.name
        })


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur')
    title = models.CharField(max_length=50, verbose_name='Titre')
    email = models.EmailField(null=True, blank=True)
    body = models.TextField(max_length=100, verbose_name='Contenu', null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE, null=True, blank=True) # (1)
    approved = models.BooleanField(default=False, verbose_name='Approuvé')

    def __str__(self):
        return self.title[:50]

    def get_delete_item(self):
        return reverse('delete-comment', kwargs={'id': self.id})

    def get_update_item(self):
        return reverse('update-comment', kwargs={'id': self.id})

# (1)
# related_name = inverse d'une foreign key (la classe Post peut accéder aux attributs de la classe Comment)


class Favorite(models.Model):
    favorite_posts = models.ManyToManyField(Post)
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Membre', null=True)

