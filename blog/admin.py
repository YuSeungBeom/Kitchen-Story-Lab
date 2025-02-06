from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nickname', 'email', 'created_at']
    search_fields = ['username', 'nickname', 'email']
    list_filter = ['is_active', 'is_staff']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'view_count', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    raw_id_fields = ['author']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at']
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    search_fields = ['content']

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']

@admin.register(Scrap)
class ScrapAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['post', 'cooking_time', 'difficulty', 'created_at']
    list_filter = ['difficulty']

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ['post', 'tip_category', 'created_at']
    search_fields = ['key_points']