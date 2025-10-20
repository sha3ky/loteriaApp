# from django.shortcuts import render

# from rest_framework import viewsets
# from .models import Personas
# from .serializers import PersonasSerializer

# class PersonasViewSet(viewsets.ModelViewSet):  # Usar ModelViewSet para manejar todas las operaciones CRUD
#     queryset = Personas.objects.all()
#     serializer_class = PersonasSerializer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Personas, Producto
from .serializers import ProductoSerializer
from django.views.decorators.http import require_http_methods
import json, os
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


# //eliminar producto
class ProductoDeleteView(APIView):
    def delete(self, request, producto_id):
        try:
            # Log para seguimiento
            print(f"Intentando eliminar el producto con ID: {producto_id}")

            # Buscar el producto por ID
            producto = Producto.objects.get(id=producto_id)
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
            print("El producto no existe en la base de datos.")
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
            # Extraer datos del request
            nombre = request.data.get("nombre")
            descripcion = request.data.get("descripcion")
            cantidad = request.data.get("cantidad", None)  # Opcional
            precio = request.data.get("precio", None)  # Opcional
            imagen_base64 = request.data.get("imagen_base64", None)  # Opcional

            # Convertir cantidad y precio si son válidos
            cantidad = int(cantidad) if cantidad else None
            precio = float(precio) if precio else None

            # Crear el producto en la base de datos
            producto = Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                cantidad=cantidad if cantidad else None,
                precio=precio if precio else None,
                imagen_base64=imagen_base64,
            )

            return Response(
                {
                    "message": "Producto creado exitosamente!",
                    "producto_id": producto.id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # Manejo genérico de errores
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ver todos los productos de la base de datos
class ProductoListView(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# update persona en la tabla
class UpdatePersonaView(APIView):
    def put(self, request, persona_id):
        try:
            # Retrieve the persona instance
            persona = Personas.objects.get(id=persona_id)

            # Parse and update fields dynamically
            for key, value in request.data.items():
                setattr(persona, key, value)

            # Save the updated persona
            persona.save()

            return Response(
                {"message": "Persona updated successfully!"}, status=status.HTTP_200_OK
            )
        except Personas.DoesNotExist:
            return Response(
                {"error": "Persona not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeletePersonaView(APIView):
    def delete(self, request, persona_id):
        try:
            # Busca la persona por ID
            persona = Personas.objects.get(id=persona_id)

            # Elimina la persona
            persona.delete()

            return Response(
                {"message": "Persona eliminada exitosamente!"},
                status=status.HTTP_200_OK,
            )
        except Personas.DoesNotExist:
            return Response(
                {"error": "Persona no encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:  # Check if the user is an admin
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                print("refreshToken", refresh)
                return Response(
                    {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "role": "admin",
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@csrf_exempt
def number_status(request):
    if request.method == "GET":
        try:
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
                for persona in Personas.objects.all()
            }
            return JsonResponse(numbers_status)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def get_winner(request, winner_id):
    if request.method == "GET":
        try:
            persona = Personas.objects.get(numero_seleccionado=winner_id)
            winner = {
                "nombre_completo": (
                    f"{persona.nombre} {persona.apellido[0].upper()}."
                    if persona.apellido
                    else persona.nombre
                ),
                "numero": persona.numero_seleccionado,
            }
            return JsonResponse(winner)
        except Personas.DoesNotExist:
            return JsonResponse({"error": "Ganador no encontrado"}, status=404)
        except Exception as e:
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
        print("Paso 1: Iniciando función reserve_number")
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
        if Personas.objects.filter(numero_seleccionado=number).exists():
            print(f"Error: El número {number} ya está reservado.")
            return JsonResponse({"error": "Este número ya está reservado."}, status=400)

        # Crear una nueva entrada en la base de datos
        print("Paso 4: Creando nueva entrada en la base de datos")
        persona = Personas(
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
            # Consulta todos los datos de la tabla Personas
            personas_data = list(
                Personas.objects.values(
                    "id",
                    "nombre",
                    "apellido",
                    "telefono",
                    "creado_en",
                    "numero_seleccionado",
                    "correo",
                    "descripcion",
                    "comentarios",
                )
            )
            return JsonResponse(
                personas_data, safe=False
            )  # Retorna la lista de objetos
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)
