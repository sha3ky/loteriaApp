from rest_framework import serializers
from .models import Personas, Producto, Cliente, UserProfile, ConfiguracionCliente, Sorteo

class PersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = [
            "id",
            "cliente",  # ← NUEVO
            "nombre",
            "apellido", 
            "numero_seleccionado",
            "telefono",
            "correo",
            "descripcion",
            "comentarios",
            "creado_en",  # ← NUEVO
        ]

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "id", 
            "cliente",  # ← NUEVO
            "nombre", 
            "descripcion", 
            "cantidad", 
            "precio", 
            "imagen_base64"
        ]

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre", "token", "creado_en"]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "user", "cliente", "rol", "creado_en"]

class ConfiguracionClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionCliente
        fields = [
            "id",
            "cliente",
            "fecha_final_countdown",
            "horas_extension_countdown",
            "logo_url", 
            "logo_base64",
            "color_principal",
            "color_secundario",
            "mostrar_boton_demo",
            "texto_boton_demo",
            "auto_girar_ruleta", 
            "intervalo_auto_girar",
            "texto_countdown",
            "texto_ganador",
            "texto_intentar_otra_vez",
            "creado_en",
            "actualizado_en",
        ]

class SorteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorteo
        fields = ["id", "cliente", "numero_ganador", "fecha", "admin"]