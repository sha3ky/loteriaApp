from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Personas
from .models import Producto

admin.site.register(Personas)  # 
admin.site.register(Producto)