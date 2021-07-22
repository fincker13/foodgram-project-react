from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Регистрация пользователя в админке с полем role"""
    list_display = ('username',)


admin.site.register(User, UserAdmin)
