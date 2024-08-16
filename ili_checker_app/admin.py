from django.contrib import admin
from ili_checker_app.models import *

# Register your models here.
ili_checker_model = [
    Tarea,
    Modelo,
    Regla
]
admin.site.register(ili_checker_model)
