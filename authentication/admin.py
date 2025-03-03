from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import InterfaceUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = InterfaceUser
        fields = ('email', 'username', 'name')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = InterfaceUser
        fields = ('email', 'username', 'name')

class InterfaceUserAdmin(UserAdmin):
    form = CustomUserChangeForm 
    add_form = CustomUserCreationForm
    
    list_display = ('email', 'username', 'name', 'is_admin')
    list_filter = ('groups',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'username')}),
        ('Groups and Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',),
            'description': 'User groups and specific permissions'
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'username', 'password1', 'password2', 'groups'),
        }),
    )
    
    search_fields = ('email', 'name', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('email',)
        return self.readonly_fields

admin.site.register(InterfaceUser, InterfaceUserAdmin)
