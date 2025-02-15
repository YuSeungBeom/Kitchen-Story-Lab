# Generated by Django 5.1.5 on 2025-02-05 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('blog', '0002_category_tag_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='이 사용자가 속한 그룹입니다.', related_name='blog_user_set', related_query_name='blog_user', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='이 사용자에 대한 특정 권한입니다.', related_name='blog_user_permissions', related_query_name='blog_user_permission', to='auth.permission'),
        ),
    ]
