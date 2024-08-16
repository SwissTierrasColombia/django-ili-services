import os
import shutil
from django.db import models
from django.contrib.auth.models import User


class Tarea(models.Model):
    SELECCION_ESTADOS = {
        "Completado": "Completado",
        "En_Proceso": "En proceso",
        "Pendiente": "Pendiente",
        "Error": "Error"
    }
    
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True)
    estado = models.CharField(
        max_length=10,
        choices=SELECCION_ESTADOS,
        default="Pendiente"
    )
    productos = models.TextField()
    nombre = models.TextField()
    directorio = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def delete(self, *args, **kwargs):
        path = str(self.directorio)

        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                raise Exception(str(e))

        super().delete(*args, **kwargs)

    class Meta:
        db_table = "tarea"

    def __str__(self):
        return self.nombre


class Modelo(models.Model):
    nombre = models.TextField()
    descripcion = models.TextField()
    iliname = models.TextField(unique=True)

    class Meta:
        db_table = "modelo"

    def __str__(self):
        return self.nombre

class Regla(models.Model):
    query = models.TextField()
    nombre = models.TextField()
    descripcion = models.TextField()
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "regla"

    def __str__(self):
        return self.nombre
