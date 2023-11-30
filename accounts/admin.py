from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import IQOption

class IQOptionInline(admin.StackedInline):
    model = IQOption
    can_delete = False
    verbose_name_plural = 'IQ Option'
    readonly_fields = ('iqoption_real_saldo', 'iqoption_practice_saldo')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.can_delete = False
        return formset

class CustomUserAdmin(BaseUserAdmin):
    inlines = (IQOptionInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)