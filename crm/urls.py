"""
URL configuration for crm project.

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
from django.contrib import admin
from django.urls import path
from clientes import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Administración de Django
    path('login/', views.inicio_sesion, name='login'),  # Iniciar sesión
    path('logout/', views.cerrar_sesion, name='logout'),  # Cerrar sesión
    path('registro/', views.registro, name='registro'),  # Registro de usuarios
    path('', views.home, name='home'),  # Página de inicio
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('clientes/', views.listar_clientes, name='listar_clientes'),  # Listar clientes
    path('crear/', views.crear_cliente, name='crear_cliente'),  # Crear cliente
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),  # Editar cliente
    path('eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),  # Eliminar cliente
    path('enviar_correo/<int:id>/', views.enviar_correo_cliente, name='enviar_correo_cliente'),  # Enviar correo al cliente
]
