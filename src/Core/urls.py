from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.posts_list, name='index'),
    path('blog/<slug>', views.post_detail, name='post-detail'),
    path('<id>/delete', views.delete_commnent, name='delete-comment'),
    path('<id>/update', views.update_comment, name='update-comment'),
    path('category/<category>', views.category_list, name='category-list'),
    path('search/', views.search, name='search'),
    path('accounts/', include('Accounts.urls', namespace='accounts')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

