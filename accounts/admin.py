from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import IQOption
from iqoption.tasks import login_iqoption, atualizar_saldo_real, atualizar_saldo_pratica, atualizar_ativos_binarios

class IQOptionInline(admin.StackedInline):
    model = IQOption
    can_delete = False
    verbose_name_plural = 'IQ Option'
    fields = (
        'iqoption_permitir', 
        'iqoption_email', 
        'iqoption_password', 
        'iqoption_type', 
        'iqoption_real_saldo_display', 
        'iqoption_practice_saldo_display'
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.can_delete = False
        return formset

    def get_readonly_fields(self, request, obj=None):
        return ('iqoption_real_saldo_display', 'iqoption_practice_saldo_display')

class CustomUserAdmin(BaseUserAdmin):
    inlines = (IQOptionInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if hasattr(obj, 'iqoption'):
            IQAPI = login_iqoption(obj.iqoption)
            atualizar_saldo_real(obj.iqoption, IQAPI)
            atualizar_saldo_pratica(obj.iqoption, IQAPI)
            atualizar_ativos_binarios(obj.iqoption, IQAPI)
            obj.iqoption.save()
            

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)