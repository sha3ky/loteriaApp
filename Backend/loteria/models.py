from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    token = models.CharField(max_length=50, unique=True)  # ID único por frontend
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre


# models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=[
        ('admin', 'Administrador'),
        ('editor', 'Editor'), 
        ('visor', 'Solo lectura')
    ], default='editor')
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'cliente']  # ✅ Un usuario solo en un cliente
    
    def __str__(self):
        return f"{self.user.username} - {self.cliente.nombre}"


class Personas(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # ← NUEVO
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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # ← NUEVO
    nombre = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagen_base64 = models.TextField(
        null=True, blank=True
    )  # Almacena la imagen en Base64

    def __str__(self):
        return self.nombre

# models.py
class ConfiguracionCliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='configuracion')
    
    # Configuraciones de cuenta atrás
    fecha_final_countdown = models.DateTimeField(null=True, blank=True)
    horas_extension_countdown = models.IntegerField(default=2)  # Horas a añadir cuando termina
    
    # Configuraciones de apariencia
    logo_url = models.URLField(blank=True, null=True)
    logo_base64 = models.TextField(blank=True, null=True)  # O almacenar logo en base64
    color_principal = models.CharField(max_length=7, default='#FFFFFF')  # Hex color
    color_secundario = models.CharField(max_length=7, default='#000000')
    
    # Configuraciones de funcionalidad
    mostrar_boton_demo = models.BooleanField(default=True)
    texto_boton_demo = models.CharField(max_length=50, default="Modo Demo")
    auto_girar_ruleta = models.BooleanField(default=False)
    intervalo_auto_girar = models.IntegerField(default=60)  # Minutos
    
    # Textos personalizables
    texto_countdown = models.CharField(
        max_length=200, 
        default="Empezamos la cuenta atras. Gracias por la paciencia..."
    )
    texto_ganador = models.CharField(
        max_length=200,
        default="La ganadora o el Ganador es"
    )
    texto_intentar_otra_vez = models.CharField(
        max_length=200,
        default="Vuelve a probar otra vez. Sin número asignado."
    )
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuración de {self.cliente.nombre}"


class Sorteo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_ganador = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]  # ✅ Mismo rango que personas
    )
    fecha = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-fecha']  # ✅ Ordenar por fecha descendente
    
    def __str__(self):
        return f"Sorteo {self.id} - {self.cliente.nombre} - Ganador: {self.numero_ganador}"