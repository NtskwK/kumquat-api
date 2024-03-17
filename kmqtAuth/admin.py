from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from kmqtAuth.models import KmqtUser


# Register your models here.
class KmqtAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'roles', 'user_permissions')}),
        (_('Important dates'), {'fields': ('date_joined',)})
    )

    list_display = ('username', 'email', 'is_active', 'last_login', 'date_joined', 'id', 'roles')
    list_display_links = ('username', 'email', 'last_login', 'date_joined', 'id', 'roles')
    search_fields = ('username', 'email')


admin.site.register(KmqtUser, KmqtAdmin)
