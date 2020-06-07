from django.contrib import admin
from django_login_history.models import Login


class ReadOnlyModelAdmin(admin.ModelAdmin):
    actions = None
    model = Login

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return (request.method in ['GET', 'HEAD'] and
                super().has_change_permission(request, obj))

    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.
admin.site.register(Login, ReadOnlyModelAdmin)
