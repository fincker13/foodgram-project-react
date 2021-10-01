# Generated by Django 3.0.5 on 2021-09-30 21:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_v1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(through='api_v1.Amount', to='api_v1.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(to='api_v1.Tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorites', to='api_v1.Recipes', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddField(
            model_name='amount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.Ingredient'),
        ),
        migrations.AddField(
            model_name='amount',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.Recipes'),
        ),
    ]