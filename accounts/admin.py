from django.contrib import admin
from accounts.models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin

class AccountConfig(UserAdmin):
    list_display = ('email', 'first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileConfig(admin.ModelAdmin):
    list_display = ('user', )
# Register your models here.
admin.site.register(Account,AccountConfig)
admin.site.register(UserProfile,UserProfileConfig)