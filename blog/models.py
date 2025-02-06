from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='blog_user_set',
        blank=True,
        help_text='이 사용자가 속한 그룹입니다.',
        related_query_name='blog_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='blog_user_permissions',
        blank=True,
        help_text='이 사용자에 대한 특정 권한입니다.',
        related_query_name='blog_user_permission'
    )

    class Meta:
        db_table = 'users'

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[('draft', '임시저장'), ('published', '발행됨')],
        default='published'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        ordering = ['order', 'name']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tags'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_likes'
        unique_together = ['post', 'user']


class Scrap(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scraps'
        unique_together = ['post', 'user']


class Recipe(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    serving_size = models.CharField(max_length=50, null=True, blank=True)
    cooking_time = models.IntegerField(null=True)
    difficulty = models.CharField(
        max_length=10, 
        choices=[('easy', '쉬움'), ('medium', '보통'), ('hard', '어려움')]
    )
    ingredients = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recipes'

class Tip(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    tip_category = models.CharField(max_length=50)
    key_points = models.TextField()
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tips'