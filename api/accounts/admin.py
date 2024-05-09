from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'mobileNo', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobileNo', 'profile_pic', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    list_display = ('username', 'email', 'mobileNo', 'is_staff')
    search_fields = ('username', 'email', 'mobileNo')
    filter_horizontal = ('groups', 'user_permissions',)

class CustomGroupAdmin(GroupAdmin):  # Inherits from GroupAdmin
    filter_horizontal = ('permissions',)

# Unregister the default Group admin
admin.site.unregister(Group)

# Register your CustomUserAdmin with the admin site
admin.site.register(CustomUser, CustomUserAdmin)

# Register your CustomGroupAdmin with the admin site
admin.site.register(Group, CustomGroupAdmin)
