from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

admin.site.register(User, UserAdmin)