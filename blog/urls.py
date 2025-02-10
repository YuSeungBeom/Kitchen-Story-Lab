from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('write/', views.PostCreateView.as_view(), name='post_write'),
    path('post/<int:post_pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<int:post_pk>/comment/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('search/', views.SearchView.as_view(), name='post_search'),
]
