from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=50,
        choices=[
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
            ('Pendiente', 'Pendiente')
        ],
        default='Activo'
    )

    def __str__(self):
        return self.nombre

class ActividadCliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)  # e.g., "Creado", "Editado", "Eliminado"
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} - {self.cliente.nombre} - {self.fecha}"
