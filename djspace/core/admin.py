from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from djspace.core.models import UserProfile, GenericChoice

class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')

admin.site.register(GenericChoice, GenericChoiceAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = (
        'user__last_name','user__first_name','user__email','user__username'
    )

admin.site.register(UserProfile, UserProfileAdmin)

# override django admin user display
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)