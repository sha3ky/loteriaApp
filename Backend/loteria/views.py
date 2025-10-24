# from django.shortcuts import render

# from rest_framework import viewsets
# from .models import Personas
# from .serializers import PersonasSerializer

# class PersonasViewSet(viewsets.ModelViewSet):  # Usar ModelViewSet para manejar todas las operaciones CRUD
#     queryset = Personas.objects.all()
#     serializer_class = PersonasSerializer
import random
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
""" from channels.layers import get_channel_layer  # ✅ CORRECTO"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Personas, 
    Producto, 
    Sorteo,           
    Cliente,          
    UserProfile,      
    ConfiguracionCliente  
)
from .serializers import ProductoSerializer
from django.views.decorators.http import require_http_methods
import json, os
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import requests
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
# print(f"TELEGRAM_TOKEN desde settings: {settings.TELEGRAM_TOKEN}")
# print(f"TELEGRAM_CHAT_ID desde settings: {settings.TELEGRAM_CHAT_ID}")


""" class GirarRuletaView(APIView): WEBSOCKETS 
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cliente_token = request.headers.get('X-Cliente-Token')
        if not cliente_token:
            return Response({"error": "Se requiere X-Cliente-Token"}, status=400)
        
        cliente = Cliente.objects.get(token=cliente_token)
        
        # Verificar que el usuario es staff
        if not request.user.is_staff:
            return Response({"error": "No autorizado"}, status=403)
        
        ganador = random.randint(1, 50)
        
        sorteo = Sorteo.objects.create(
            cliente=cliente,
            numero_ganador=ganador,
            fecha=timezone.now(),
            admin=request.user
        )
        
         # Notificar via WebSocket (DENTRO de la función)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'ruleta_cliente_{cliente.id}',
            {
                'type': 'ruleta_girada',
                'ganador': ganador,
                'sorteo_id': sorteo.id,
                'fecha': sorteo.fecha.isoformat()
            }
        ) 
        
        # Return DENTRO de la función
        return Response({'ganador': ganador, 'sorteo_id': sorteo.id})

 """
class GirarRuletaView(APIView):
    def get(self, request):
        try:
            cliente_token = request.headers.get('X-Cliente-Token') or request.GET.get('token')
            if not cliente_token:
                return Response({"error": "Se requiere token"}, status=400)
            
            cliente = Cliente.objects.get(token=cliente_token)
            
            ganador = random.randint(1, 50)
            
            sorteo = Sorteo.objects.create(
                cliente=cliente,
                numero_ganador=ganador,
                fecha=timezone.now(),
            )
            
            return Response({'ganador': ganador})
            
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=404)
        except Exception as e:
            print(f"❌ Error en girar-ruleta: {e}")
            return Response({"error": "Error interno del servidor"}, status=500)
            
# //eliminar producto
class ProductoDeleteView(APIView):
    def delete(self, request, producto_id):
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return Response(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return Response(
                    {"error": "Cliente no encontrado."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # PASO 3: Buscar el producto SOLO de este cliente
            print(f"Paso 3: Buscando producto {producto_id} para {cliente.nombre}")
            producto = Producto.objects.get(id=producto_id, cliente=cliente)  # ← FILTRAR POR CLIENTE
            print(f"Producto encontrado: {producto.nombre}")

            # Eliminar la imagen del sistema de archivos si existe
            # if producto.filepath:
            #     image_path = os.path.join(settings.MEDIA_ROOT, producto.filepath)
            #     print(f"Intentando eliminar la imagen en: {image_path}")

            #     if os.path.exists(image_path):
            #         os.remove(image_path)
            #         print("Imagen eliminada exitosamente.")
            #     else:
            #         print("La imagen no existe en el sistema de archivos.")

            # Eliminar el producto de la base de datos
            producto.delete()
            print("Producto eliminado de la base de datos.")

            return Response(
                {"message": "Producto eliminado exitosamente!"},
                status=status.HTTP_200_OK,
            )

        except Producto.DoesNotExist:
            print(f"Error: Producto {producto_id} no encontrado para {cliente.nombre}")
            return Response(
                {"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error inesperado: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductoCreateView(APIView):
    def post(self, request):
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return Response(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return Response(
                    {"error": "Cliente no encontrado."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # PASO 3: Extraer datos del request
            nombre = request.data.get("nombre")
            descripcion = request.data.get("descripcion")
            cantidad = request.data.get("cantidad", None)
            precio = request.data.get("precio", None)
            imagen_base64 = request.data.get("imagen_base64", None)

            # Convertir cantidad y precio si son válidos
            cantidad = int(cantidad) if cantidad else None
            precio = float(precio) if precio else None

            # PASO 4: Crear el producto ASOCIADO AL CLIENTE
            print("Paso 4: Creando producto para el cliente")
            producto = Producto.objects.create(
                cliente=cliente,  # ← ASIGNAR CLIENTE
                nombre=nombre,
                descripcion=descripcion,
                cantidad=cantidad if cantidad else None,
                precio=precio if precio else None,
                imagen_base64=imagen_base64,
            )

            print(f"Paso 5: Producto creado exitosamente - {producto.nombre} para {cliente.nombre}")
            return Response(
                {
                    "message": "Producto creado exitosamente!",
                    "producto_id": producto.id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(f"Error general: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# ver todos los productos de la base de datos

class ProductoListView(APIView):
    def get(self, request):
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return Response(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return Response(
                    {"error": "Cliente no encontrado."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # PASO 3: Consultar solo los productos de ESTE cliente
            print("Paso 3: Consultando productos del cliente")
            productos = Producto.objects.filter(cliente=cliente)  # ← FILTRAR POR CLIENTE
            serializer = ProductoSerializer(productos, many=True)
            
            print(f"Paso 4: Encontrados {len(productos)} productos para {cliente.nombre}")
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error general: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# update persona en la tabla

class UpdatePersonaView(APIView):
    def put(self, request, persona_id):
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return Response(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return Response(
                    {"error": "Cliente no encontrado."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # PASO 3: Buscar la persona SOLO de este cliente
            print(f"Paso 3: Buscando persona {persona_id} para {cliente.nombre}")
            persona = Personas.objects.get(id=persona_id, cliente=cliente)  # ← FILTRAR POR CLIENTE

            # PASO 4: Actualizar campos dinámicamente
            for key, value in request.data.items():
                setattr(persona, key, value)

            # Guardar la persona actualizada
            persona.save()
            print(f"Paso 4: Persona {persona_id} actualizada exitosamente")

            return Response(
                {"message": "Persona updated successfully!"}, status=status.HTTP_200_OK
            )
        except Personas.DoesNotExist:
            print(f"Error: Persona {persona_id} no encontrada para {cliente.nombre}")
            return Response(
                {"error": "Persona not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error general: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeletePersonaView(APIView):
    def delete(self, request, persona_id):
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return Response(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return Response(
                    {"error": "Cliente no encontrado."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # PASO 3: Buscar la persona SOLO de este cliente
            print(f"Paso 3: Buscando persona {persona_id} para {cliente.nombre}")
            persona = Personas.objects.get(id=persona_id, cliente=cliente)  # ← FILTRAR POR CLIENTE

            # Eliminar la persona
            persona.delete()
            print(f"Paso 4: Persona {persona_id} eliminada exitosamente")

            return Response(
                {"message": "Persona eliminada exitosamente!"},
                status=status.HTTP_200_OK,
            )
        except Personas.DoesNotExist:
            print(f"Error: Persona {persona_id} no encontrada para {cliente.nombre}")
            return Response(
                {"error": "Persona no encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error general: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                cliente_token = request.data.get("cliente_token")
                if not cliente_token:
                    return Response({"error": "Admin debe especificar cliente_token"}, status=400)
                
                cliente = Cliente.objects.get(token=cliente_token)
                
                # GENERAR TOKENS JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "role": "admin",
                        "cliente_id": cliente.id,
                        "cliente_nombre": cliente.nombre,
                    },
                }, status=status.HTTP_200_OK)
            
            else:
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    cliente = user_profile.cliente
                    
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "role": user_profile.rol,
                            "cliente_id": cliente.id,
                            "cliente_nombre": cliente.nombre,
                        },
                    })
                except UserProfile.DoesNotExist:
                    return Response({"error": "Usuario no tiene cliente asignado"}, status=403)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
def number_status(request):
    if request.method == "GET":
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return JsonResponse(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=400
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return JsonResponse(
                    {"error": "Cliente no encontrado."}, 
                    status=404
                )

            # PASO 3: Consultar solo las personas de ESTE cliente
            print("Paso 3: Consultando estado de números del cliente")
            numbers_status = {
                persona.id: {
                    "status": "green" if persona.numero_seleccionado else "red",
                    "nombre_completo": (
                        f"{persona.nombre} {persona.apellido[0].upper()}."
                        if persona.apellido
                        else persona.nombre
                    ),
                    "numero": persona.numero_seleccionado,
                }
                for persona in Personas.objects.filter(cliente=cliente)  # ← FILTRAR POR CLIENTE
            }
            
            print(f"Paso 4: Estado de números para {cliente.nombre} - {len(numbers_status)} registros")
            return JsonResponse(numbers_status)
        except Exception as e:
            print(f"Error general: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def get_winner(request, winner_id):
    if request.method == "GET":
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return JsonResponse(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=400
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return JsonResponse(
                    {"error": "Cliente no encontrado."}, 
                    status=404
                )

            # PASO 3: Buscar ganador SOLO para este cliente
            print(f"Paso 3: Buscando ganador {winner_id} para {cliente.nombre}")
            persona = Personas.objects.get(cliente=cliente, numero_seleccionado=winner_id)  # ← FILTRAR POR CLIENTE
            winner = {
                "nombre_completo": (
                    f"{persona.nombre} {persona.apellido[0].upper()}."
                    if persona.apellido
                    else persona.nombre
                ),
                "numero": persona.numero_seleccionado,
            }
            
            print(f"Paso 4: Ganador encontrado - {winner['nombre_completo']}")
            return JsonResponse(winner)
        except Personas.DoesNotExist:
            print(f"Error: Ganador {winner_id} no encontrado para {cliente.nombre}")
            return JsonResponse({"error": "Ganador no encontrado"}, status=404)
        except Exception as e:
            print(f"Error general: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)


def send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Mensaje enviado exitosamente.")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar mensaje a Telegram: {e}")


@csrf_exempt
@require_http_methods(["POST"])  # Asegura que solo se acepten solicitudes POST
def reserve_number(request):
    try:
        cliente_token = request.headers.get('X-Cliente-Token')
        print(f"Paso 1: Token recibido - {cliente_token}")
        # Validar que el token existe
        if not cliente_token:
            print("Error: No se proporcionó X-Cliente-Token en el header")
            return JsonResponse(
                {"error": "Se requiere el header X-Cliente-Token."}, 
                status=400
            )
        # PASO 2: Buscar el cliente en la base de datos
        try:
            cliente = Cliente.objects.get(token=cliente_token)
            print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
        except Cliente.DoesNotExist:
            print(f"Error: Cliente con token {cliente_token} no encontrado")
            return JsonResponse(
                {"error": "Cliente no encontrado."}, 
                status=404
            )

        print("Paso 3: Iniciando función reserve_number")
        # Parsear los datos del cuerpo de la solicitud
        data = json.loads(request.body)
        print(f"Paso 2: Datos recibidos - {data}")

        # Validar los datos requeridos
        required_fields = ["number", "name", "surname"]
        for field in required_fields:
            if field not in data or not data[field]:
                print(f"Error: El campo {field} es obligatorio.")
                return JsonResponse(
                    {"error": f"El campo {field} es obligatorio."}, status=400
                )

        # Buscar si ya existe una persona asociada con el número
        number = data["number"]
        print(f"Paso 3: Verificando si el número {number} ya está reservado")
        if Personas.objects.filter(cliente=cliente,numero_seleccionado=number).exists():
            print(f"Error: El número {number} ya está reservado.")
            return JsonResponse({"error": "Este número ya está reservado."}, status=400)    

        # Crear una nueva entrada en la base de datos
        print("Paso 4: Creando nueva entrada en la base de datos")
        persona = Personas(
            cliente=cliente,  # ← ESTA LÍNEA ES CLAVE
            nombre=data["name"],
            apellido=data["surname"],
            telefono=data.get("phone", ""),  # Opcional
            correo=data.get("email", ""),  # Opcional
            numero_seleccionado=number,
        )
        persona.save()
        print(f"Paso 5: Persona creada exitosamente - {persona}")

        # Enviar mensaje a Telegram
        print("Paso 6: Enviando mensaje a Telegram")
        TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
        TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
        message = (
            f"🎉 <b>Reserva Exitosa</b> 🎉\n"
            f"<b>Nombre:</b> {persona.nombre}\n"
            f"<b>Apellido:</b> {persona.apellido}\n"
            f"<b>Número:</b> {persona.numero_seleccionado}"
        )
        send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message)
        print("Paso 7: Mensaje enviado a Telegram con éxito")

        # Retornar una respuesta exitosa
        print("Paso 8: Retornando respuesta exitosa")
        return JsonResponse({"message": "Número reservado exitosamente."}, status=201)

    except json.JSONDecodeError as e:
        print(f"Error de JSON: {e}")
        return JsonResponse({"error": "Datos inválidos o mal formateados."}, status=400)
    except Exception as e:
        print(f"Error general: {e}")
        return JsonResponse({"error": f"Ocurrió un error: {str(e)}"}, status=500)


def get_allData(request):
    if request.method == "GET":
        try:
            # PASO 1: Obtener token del header
            cliente_token = request.headers.get('X-Cliente-Token')
            print(f"Paso 1: Token recibido - {cliente_token}")
            
            # Validar que el token existe
            if not cliente_token:
                print("Error: No se proporcionó X-Cliente-Token en el header")
                return JsonResponse(
                    {"error": "Se requiere el header X-Cliente-Token."}, 
                    status=400
                )
            
            # PASO 2: Buscar el cliente
            try:
                cliente = Cliente.objects.get(token=cliente_token)
                print(f"Paso 2: Cliente encontrado - {cliente.nombre}")
            except Cliente.DoesNotExist:
                print(f"Error: Cliente con token {cliente_token} no encontrado")
                return JsonResponse(
                    {"error": "Cliente no encontrado."}, 
                    status=404
                )

            # PASO 3: Consultar solo las personas de ESTE cliente
            print("Paso 3: Consultando personas del cliente")
            personas_data = list(
                Personas.objects.filter(cliente=cliente).values(  # ← FILTRAR POR CLIENTE
                    "id",
                    "nombre",
                    "apellido",
                    "telefono",
                    "creado_en",
                    "numero_seleccionado",
                    "correo",
                    "comentarios",
                )
            )
            
            print(f"Paso 4: Encontradas {len(personas_data)} personas para {cliente.nombre}")
            return JsonResponse(
                personas_data, safe=False
            )  # Retorna la lista de objetos

        except Exception as e:
            print(f"Error general: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def obtener_configuracion_cliente(request):

    try:
        cliente_token = request.GET.get('token')
        
        # Validar que el token existe
        if not cliente_token:
            return JsonResponse(
                {"error": "Se requiere el parámetro 'token'."}, 
                status=400
            )
        
        # Buscar el cliente
        cliente = Cliente.objects.get(token=cliente_token)
        
        # Obtener o crear la configuración
        configuracion, created = ConfiguracionCliente.objects.get_or_create(cliente=cliente)
        
        if created:
            print(f"✅ Configuración creada para cliente: {cliente.nombre}")
        
        return JsonResponse({
            # Cuenta atrás
            'fecha_final_countdown': configuracion.fecha_final_countdown.isoformat() if configuracion.fecha_final_countdown else None,
            'horas_extension_countdown': configuracion.horas_extension_countdown,
            
            # Apariencia
            'logo_url': configuracion.logo_url,
            'logo_base64': configuracion.logo_base64,
            'color_principal': configuracion.color_principal,
            'color_secundario': configuracion.color_secundario,
            
            # Funcionalidad
            'mostrar_boton_demo': configuracion.mostrar_boton_demo,
            'texto_boton_demo': configuracion.texto_boton_demo,
            'auto_girar_ruleta': configuracion.auto_girar_ruleta,
            'intervalo_auto_girar': configuracion.intervalo_auto_girar,
            
            # Textos
            'texto_countdown': configuracion.texto_countdown,
            'texto_ganador': configuracion.texto_ganador,
            'texto_intentar_otra_vez': configuracion.texto_intentar_otra_vez,
            
            # Metadata
            'creado_en': configuracion.creado_en.isoformat(),
            'actualizado_en': configuracion.actualizado_en.isoformat(),
        })
        
    except Cliente.DoesNotExist:
        return JsonResponse(
            {"error": "Cliente no encontrado."}, 
            status=404
        )
    except Exception as e:
        print(f"Error en obtener_configuracion_cliente: {e}")
        return JsonResponse(
            {"error": "Error interno del servidor."}, 
            status=500
        )


@csrf_exempt
def guardar_configuracion_cliente(request):
    try:
        
        if request.method != 'POST':
            return JsonResponse({"error": "Método no permitido. Solo POST."}, status=405)
        
        # ✅ Obtener token del header
        cliente_token = request.headers.get('X-Cliente-Token') or request.headers.get('Authorization')
        
        # Limpiar si viene con "Bearer "
        if cliente_token and cliente_token.startswith('Bearer '):
            cliente_token = cliente_token[7:]
        
        if not cliente_token:
            return JsonResponse({"error": "Se requiere el header 'X-Cliente-Token'."}, status=400)
        
        # Buscar el cliente
        cliente = Cliente.objects.get(token=cliente_token)
        
        # Obtener o crear la configuración
        configuracion, created = ConfiguracionCliente.objects.get_or_create(cliente=cliente)
        
        # Actualizar campos según los datos recibidos
        data = json.loads(request.body)
        # Cuenta atrás
        if 'fecha_final_countdown' in data:
            configuracion.fecha_final_countdown = data['fecha_final_countdown']
        if 'horas_extension_countdown' in data:
            configuracion.horas_extension_countdown = data['horas_extension_countdown']
        
        # Apariencia
        if 'logo_url' in data:
            configuracion.logo_url = data['logo_url']
        if 'logo_base64' in data:
            configuracion.logo_base64 = data['logo_base64']
        if 'color_principal' in data:
            configuracion.color_principal = data['color_principal']
        if 'color_secundario' in data:
            configuracion.color_secundario = data['color_secundario']
        
        # Funcionalidad
        if 'mostrar_boton_demo' in data:
            configuracion.mostrar_boton_demo = data['mostrar_boton_demo']
        if 'texto_boton_demo' in data:
            configuracion.texto_boton_demo = data['texto_boton_demo']
        if 'auto_girar_ruleta' in data:
            configuracion.auto_girar_ruleta = data['auto_girar_ruleta']
        if 'intervalo_auto_girar' in data:
            configuracion.intervalo_auto_girar = data['intervalo_auto_girar']
        
        # Textos
        if 'texto_countdown' in data:
            configuracion.texto_countdown = data['texto_countdown']
        if 'texto_ganador' in data:
            configuracion.texto_ganador = data['texto_ganador']
        if 'texto_intentar_otra_vez' in data:
            configuracion.texto_intentar_otra_vez = data['texto_intentar_otra_vez']
        
        configuracion.save()
        
        return JsonResponse({
            "mensaje": "✅ Configuración guardada correctamente",
            "actualizado_en": configuracion.actualizado_en.isoformat()
        })
        
    except Cliente.DoesNotExist:
        return JsonResponse(
            {"error": "Cliente no encontrado."}, 
            status=404
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "JSON inválido en el cuerpo de la solicitud."}, 
            status=400
        )
    except Exception as e:
        print(f"Error en guardar_configuracion_cliente: {e}")
        return JsonResponse(
            {"error": "Error interno del servidor."}, 
            status=500
        )