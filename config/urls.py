from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/posts/', permanent=True)),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('posts/', include('apps.posts.urls', 'namespace=posts')),
    path('recipes/', include('apps.recipes.urls')),
    path('tips/', include('apps.tips.urls')),
    path('interactions/', include('apps.interactions.urls')),
] 