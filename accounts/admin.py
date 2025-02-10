from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'nickname', 'email', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'profile_image', 'bio')}),
    )

admin.site.register(User, CustomUserAdmin)