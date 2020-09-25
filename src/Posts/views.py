from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Post, Category, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import resolve, reverse_lazy, reverse
from .forms import AddCommentForm, CommentUpdateForm

website_title = 'Django Addict'

# Fonction retournant le name de l'url
def get_url_name(url):
    return resolve(url).url_name


# Page d'acceuil
def posts_list(request):
    qs = Post.objects.all() # Tous les posts
    featured_posts = Post.objects.filter(featured=True) # Post mis en avant (3 posts)
    star_post = Post.objects.filter(star=True).first() # Post du jour - Un seul post

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 4)
    try:
        pg = paginator.page(page)
    except PageNotAnInteger:
        pg = paginator.page(1)
    except EmptyPage:
        pg = paginator.page(paginator.num_pages)
    # Fin pagination

    context = {
        # 'posts': qs,
        'title': 'Django Addict',
        'featured_posts': featured_posts,
        'star_post': star_post,
        'pg': pg, # On injecte le paginator plutot que le queryset
    }
    return render(request, 'posts/blog-listing.html', context=context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = AddCommentForm(request.POST or None, initial={'email': request.user.email} if request.user.is_authenticated else '') # Inital = populé un champ du formulaire

    # qs = get_list_or_404(Comment, post__pk=post.pk)
    qs = Comment.objects.filter(post__pk=post.pk)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={'slug': post.slug}))

    context = {
        'title': post.title,
        'post': post,
        'form': form,
        'comments': qs,

    }
    return render(request, 'posts/blog-article.html', context=context)


# Posts triés par catégorie
def category_list(request, category):
    qs = get_list_or_404(Post, category__name=category)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 4)
    try:
        pg = paginator.page(page)
    except PageNotAnInteger:
        pg = paginator.page(1)
    except EmptyPage:
        pg = paginator.page(paginator.num_pages)
    # Fin pagination

    context = {
        'title': category.capitalize(),
        'posts': qs,
        'pg': pg,
    }
    return render(request, 'posts/category-listing.html', context=context)


# Rechercher un ou des posts
def search(request):
    categories = Category.objects.all()
    qs = Post.objects.all()
    query = request.GET.get('q')  # variable qui va contenu la requete (correspond à l'attribut name du formulaire)
    if query:
        qs = qs.filter(
            Q(title__icontains=query) | Q(body__icontains=query) | Q(category__name__icontains=query)).distinct()
    context = {
        'title': f'Tous les articles - {website_title}',
        'categories': categories,
        'link_name': get_url_name(request.path), # Retourne le name de l'url
        'link_path': request.path,
        'queryset': qs

    }
    return render(request, 'posts/search-index.html', context=context)

#################
# Comments
#################


def delete_commnent(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER')) # On retroune à la page précédente (referer)


def update_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    form = CommentUpdateForm(request.POST or None, instance=comment)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('post-detail', kwargs={'slug': comment.post.slug}))

    context = {
        'title': f'Mettre à jour - {website_title}',
        'form': form
    }
    return render(request, 'posts/update-comment.html', context=context)







