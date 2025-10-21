from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Personas
from .models import Producto
from .models import Cliente 
from .models import ConfiguracionCliente
from .models import UserProfile

admin.site.register(Personas)  # 
admin.site.register(Producto)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'token', 'creado_en']
    search_fields = ['nombre', 'token']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cliente', 'rol', 'creado_en']
    list_filter = ['cliente', 'rol']

# admin.py
@admin.register(ConfiguracionCliente)
class ConfiguracionClienteAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'fecha_final_countdown', 'mostrar_boton_demo', 'actualizado_en']
    list_filter = ['mostrar_boton_demo', 'auto_girar_ruleta']
    search_fields = ['cliente__nombre']
    
    fieldsets = (
        ('Cuenta Atrás', {
            'fields': ('fecha_final_countdown', 'horas_extension_countdown', 'texto_countdown')
        }),
        ('Apariencia', {
            'fields': ('logo_url', 'logo_base64', 'color_principal', 'color_secundario')
        }),
        ('Funcionalidad', {
            'fields': ('mostrar_boton_demo', 'texto_boton_demo', 'auto_girar_ruleta', 'intervalo_auto_girar')
        }),
        ('Textos', {
            'fields': ('texto_ganador', 'texto_intentar_otra_vez')
        }),
    )