# django-ili-services

### Clone repository

```bash
git clone --recurse-submodules https://github.com/swisstierrascolombia/django-ili-services.git
```

### Create an environment

```bash
python3 -m venv .venv
```

### Activate the environment

```bash
source .venv/bin/activate
```

### Install dependences

```bash
pip install -r ./requirements.txt
```

### Install external dependences

```bash
pip install -r ./ili_checker_app/submodules/requirements.txt
```

### Create environments

Crear un archivo .env con las mismas varibales que estan definidas en el archivo de ejemplo .env.example

```bash
NAME_SU="Nombre super usuario"
EMAIL_SU="Correo del super usuario"
PASSWORD_SU="clave de acceso del super usuario"

# Actualizar según corresponda.
ILISERVICES_DB_NAME=iliservices
ILISERVICES_DB_USER=postgres
ILISERVICES_DB_PASS=admin
ILISERVICES_DB_PORT=5432
ILISERVICES_DB_HOST=localhost
```

### Run server local

Ubicarse en la ruta princial y ejecutar lo siguiente:

```bash
python manage.py migrate
python manage.py collectstatic
python create_users.py
python manage.py runserver
```

## Developers

Este proyecto depende de submodulos, por lo tanto si estas trabajando en modo local deberas ejecutar los siguientes comandos para iniciar los submodulos y descargar las ultimas actualizaciones de las dependencias.

```bash
git submodule init
git submodule update --remote --recursive
```
