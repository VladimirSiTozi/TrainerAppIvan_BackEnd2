from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import AppUser, Profile


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    list_display = ('email', 'is_active', 'is_staff')  # Fields displayed in admin list view
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'date_of_birth')  # Fields displayed in the list view
    search_fields = ('user__email', 'first_name', 'last_name')  # Allows searching by user email, first name, or last name
    ordering = ('user',)


