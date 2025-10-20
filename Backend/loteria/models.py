from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Personas(models.Model):
    nombre = models.CharField(max_length=30)  # Campo para el nombre
    apellido = models.CharField(max_length=30)  # Campo para el apellido
    telefono = models.CharField(max_length=15)  # Campo para el teléfono
    creado_en = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    numero_seleccionado = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )  # Número de 1 a 100
    correo = models.EmailField()  # Campo para el correo electrónico
    descripcion = models.TextField(
        max_length=500, blank=True
    )  # Campo para una descripción (hasta 500 caracteres)
    comentarios = models.TextField(
        max_length=500, blank=True
    )  # Campo para comentarios (hasta 500 caracteres)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"  # Método para representar el objeto


# Nuevo modelo para productos
class Producto(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagen_base64 = models.TextField(
        null=True, blank=True
    )  # Almacena la imagen en Base64

    def __str__(self):
        return self.nombre
