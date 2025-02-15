# Generated by Django 5.1.5 on 2025-02-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='조회수')),
            ],
            options={
                'verbose_name': '게시글',
                'verbose_name_plural': '게시글 목록',
                'ordering': ['-created_at'],
            },
        ),
    ]
