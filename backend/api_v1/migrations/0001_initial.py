# Generated by Django 3.0.5 on 2021-09-30 21:53

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Укажите корректное колличество продукта')], verbose_name='Колличество')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ingredient')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Еденица измерения')),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='recipes/', verbose_name='Изображение')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Укажите корретное время приготовления, минимальное время приготовления 1 миниута')], verbose_name='Время приготовления')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Tag')),
                ('color', models.CharField(blank=True, choices=[('#E26C2D', 'Завтрак'), ('#8775D2', 'Ужин'), ('#49B64E', 'Обед')], max_length=200, null=True, verbose_name='Color')),
                ('slug', models.SlugField(unique=True, verbose_name='Slag')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shopping', to='api_v1.Recipes', verbose_name='Рецепт')),
            ],
        ),
    ]
