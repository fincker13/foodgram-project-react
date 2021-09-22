from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email адрес',
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        unique=True,
        max_length=150,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
    USERNAME_FIELD = 'email'

