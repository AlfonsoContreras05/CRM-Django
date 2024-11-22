from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'fecha_creacion')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha_creacion',)

admin.site.register(Cliente, ClienteAdmin)
