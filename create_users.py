import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ili_checker_project.settings")
django.setup()

from django.contrib.auth.models import User, Group
from ili_checker_app.config.general_config import NAME_SU, EMAIL_SU, PASSWORD_SU

if not Group.objects.filter(name="Administrador").exists():
    Group.objects.create(name="Administrador")
    print(f"** Grupo 'Administrador' creado exitosamente. **")

if not User.objects.filter(username=NAME_SU).exists():
    User.objects.create_superuser(NAME_SU, EMAIL_SU, PASSWORD_SU)

    user = User.objects.get(username=NAME_SU)
    user.groups.add(Group.objects.get(name="Administrador"))
    print(f"** Usuario {NAME_SU} creado exitosamente. **")

if not User.objects.filter(username='Anonimo').exists():
    User.objects.create_user(username='Anonimo', password='Anonimo123')
    print("** Usuario Anonimo creado exitosamente. **")
