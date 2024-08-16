FROM python:3.12-slim

# Update repository OS and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    default-jdk \
    gdal-bin \
    libgdal-dev \
    ca-certificates-java \
    && rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates -f;

# Settings env
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r /app/ili_checker_app/submodules/requirements.txt

# Start the Django development server
#CMD ["/bin/sh", "-c", "python3 manage.py migrate && python3 create_super_user.py && python3 manage.py runserver 0.0.0.0:8000"]

# Start the Django production server
#CMD ["sh", "-c", "python manage.py collectstatic --no-input && python manage.py migrate && python manage.py makemigrations ili_checker_app && python manage.py migrate && python3 create_users.py && gunicorn -w 2 -b 0.0.0.0:8000 ili_checker_project.wsgi"]

# Start the Django production server with SSL
CMD ["sh", "-c", "python manage.py collectstatic --no-input && python manage.py migrate && python manage.py makemigrations ili_checker_app && python manage.py migrate && python3 create_users.py && gunicorn -w 2 -b 0.0.0.0:443 --certfile /certs/live/sitierras.com/fullchain.pem --keyfile /certs/live/sitierras.com/privkey.pem ili_checker_project.wsgi"]