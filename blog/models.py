from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True, null=True)
    profile_image = models.ImageField(
        upload_to='profiles/', 
        null=True, 
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
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
    content = HTMLField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    
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
        ordering = ['-created_at']

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 

    class Meta:
        db_table = 'categories'
        ordering = ['order', 'name']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username}의 댓글 - {self.content[:20]}'    

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_likes'
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_post_like'
            )
        ]

class Recipe(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    serving_size = models.CharField(max_length=50, null=True, blank=True)
    cooking_time = models.IntegerField(
        null=True, 
        help_text='조리 시간 (분 단위)'
    )
    difficulty = models.CharField(
        max_length=10, 
        choices=[
            ('easy', '초급'), 
            ('medium', '중급'), 
            ('hard', '고급')
        ],
        default='medium'
    )
    ingredients = models.TextField(
        null=True, 
        blank=True, 
        help_text='레시피 재료 목록'
    )
    instructions = models.TextField(
        null=True, 
        blank=True, 
        help_text='조리 과정 상세 설명'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recipes'
        ordering = ['-created_at']
