from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Personas
from .serializers import PersonasSerializer


class PersonasAPITestCase(TestCase):
    def setUp(self):
        # Crear una persona para usar en las pruebas
        self.persona = Personas.objects.create(
            nombre="Maria",
            apellido="DelMonte",
            numero_seleccionado=10,  # Valor válido para este campo
            telefono="987654321",  # Proporciona un número de teléfono válido
            correo="maria.delmonte@example.com",  # Proporciona un correo electrónico válido
        )

        # Datos válidos para las pruebas de creación
        self.valid_data = {
            "nombre": "Juan",
            "apellido": "Perez",
            "numero_seleccionado": 15,  # Este valor debe estar en el rango permitido (1-100)
            "telefono": "123456789",  # Proporciona un número de teléfono válido
            "correo": "juan.perez@example.com",  # Proporciona un correo electrónico válido
        }

        self.client = (
            APIClient()
        )  # Crea una instancia del cliente API para realizar las solicitudes

    # Método de prueba para crear una persona
    def test_create_persona(self):
        response = self.client.post("/personas/", self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Método de prueba para actualizar una persona
    def test_update_persona(self):
        updated_data = {
            "nombre": "Maria",
            "apellido": "DelMonte",
            "numero_seleccionado": 20,  # Asegúrate de que este valor también sea válido
            "telefono": "987654321",  # Proporciona un número de teléfono válido
            "correo": "maria.updated@example.com",  # Proporciona un correo electrónico válido
        }
        response = self.client.put(
            f"/personas/{self.persona.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
