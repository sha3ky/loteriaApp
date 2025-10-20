from rest_framework import serializers
from .models import Personas  # Asegúrate de importar tu modelo
from .models import Producto


class PersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = [
            "id",
            "nombre",
            "apellido",
            "numero_seleccionado",
            "telefono",
            "correo",
            "descripcion",
            "comentarios",
        ]  # Asegúrate de incluir todos los campos necesarios


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "descripcion", "cantidad", "precio", "imagen_base64"]
