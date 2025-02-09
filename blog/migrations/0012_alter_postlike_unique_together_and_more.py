# Generated by Django 5.1.5 on 2025-02-09 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_postlike_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postlike',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='scrap',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='postlike',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_post_like'),
        ),
        migrations.AddConstraint(
            model_name='scrap',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_post_scrap'),
        ),
    ]
