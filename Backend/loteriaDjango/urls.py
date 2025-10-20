"""
URL configuration for loteriaDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from loteria.views import (
    number_status,
    reserve_number,
    get_allData,
    get_winner,
    UpdatePersonaView,
    DeletePersonaView,
    ProductoListView,
    ProductoDeleteView,
    ProductoCreateView,
)  # Asegúrate de que la importación sea correcta
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

# router = DefaultRouter()
# router.register(r'personas', PersonasViewSet, basename='personas')  # Registra el ViewSet


urlpatterns = [
    path("api/productos/", ProductoCreateView.as_view(), name="producto-create"),
    path(
        "api/productos/<int:producto_id>/",
        ProductoDeleteView.as_view(),
        name="producto-delete",
    ),
    path("api/getproductos/", ProductoListView.as_view(), name="productos-list"),
    path(
        "api/delete-user/<int:persona_id>/",
        DeletePersonaView.as_view(),
        name="delete-persona",
    ),
    path(
        "api/personas/<int:persona_id>/",
        UpdatePersonaView.as_view(),
        name="update_persona",
    ),
    path("api/get-winner/<int:winner_id>/", get_winner, name="get_winner"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/get-allData/", get_allData, name="get_all_data"),
    path("api/reserve-number/", reserve_number, name="reserve_number"),  # Ruta añadida
    path("api/number-status/", number_status, name="number_status"),  # Ruta añadida
    path("admin/", admin.site.urls),  # URL para el panel de administración
    # path('', include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Sirviendo archivos estáticos y media en modo de desarrollo
if settings.DEBUG:  # Solo en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
