import os.path

# https://stackoverflow.com/a/52575537/9802768
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse

from ili_checker_app.serializer import *
from ili_checker_app.models import *
from ili_checker_app.permisions import RequestIsAllowed
from ili_checker_app.config.general_config import FORMATS_SUPPORTED
from ili_checker_app.logic.job_manager import JobManager

import mimetypes


class UsuarioViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]


class TareaViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]


class ModeloViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows models to be viewed or edited.
    """
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    permission_classes = [IsAuthenticated, RequestIsAllowed]


class ReglaViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows rules to be viewed or edited.
    """
    queryset = Regla.objects.all()
    serializer_class = ReglaSerializer
    permission_classes = [IsAuthenticated, RequestIsAllowed]


### Custom views ###

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_files(request: HttpRequest):
    """
        API endpoint that allows upload files
    """
    user = request.user

    file: UploadedFile = request.FILES.get('file')
    full_file_size: str = request.headers.get('X-File-Size')

    if not file:
        return JsonResponse(data={"message": "File is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not full_file_size:
        return JsonResponse(data={"message": "Header X-File-Size is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if mimetypes.types_map.get('.xtf') != 'application/xtf':
        # Agregar el nuevo tipo MIME
        mimetypes.add_type('application/xtf', '.xtf')

    content_type = mimetypes.guess_type(file.name)[0]
    if content_type not in FORMATS_SUPPORTED:
        return JsonResponse(
            data={"message": f"Format not supported {file.name}"},
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

    try:
        job = JobManager(file, user)
        is_file = job.receiver(int(full_file_size))
        if is_file:
            id_task = job.create_task()
            url_pdf = request.build_absolute_uri().replace('file/', f'get_report_pdf/{id_task}/')
            url_log = request.build_absolute_uri().replace('file/', f'get_report_log/{id_task}/')

            if not job.validation_xtf():
                response = {
                    "message": "El XTF no supero las validaciones.",
                    "urls": {
                        "log": url_log
                    }
                }
                return JsonResponse(data=response, status=status.HTTP_200_OK)

            response = {
                "message": "File upload successfully",
                "urls": {
                    "pdf": url_pdf,
                    "log": url_log
                }
            }
            return JsonResponse(data=response, status=status.HTTP_201_CREATED)            
        else:
            return HttpResponse(content="", status=status.HTTP_202_ACCEPTED)
    except Exception as Error:
        return JsonResponse(data={"message": f"{str(Error)}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request: HttpRequest):
    tasks_for_user = Tarea.objects.filter(usuario=request.user).order_by('-fecha_inicio')
    data = TareaSerializer(tasks_for_user, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, RequestIsAllowed])
def get_rules_for_model(request: HttpRequest, pk: int):
    rules_for_model = Regla.objects.all().filter(modelo=pk)
    data = ReglaSerializer(rules_for_model, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_is_admin(request: HttpRequest):
    if request.user.groups.filter(name='Administrador').exists():
        return Response(data={"message": "User is admin", "Admin": True}, status=status.HTTP_200_OK)
    return Response(data={"message": "User is not admin", "Admin": False}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_info_user(request: HttpRequest):
    user = UsuarioSerializer(request.user).data
    return Response(data=user, status=status.HTTP_200_OK)


# Return PDF
@api_view(['GET'])
@permission_classes([AllowAny])
def get_pdf(request: HttpRequest, pk: int):
    try:
        task = Tarea.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse(data={"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if os.path.exists(task.directorio):
        pdf_dir = os.path.join(task.directorio, 'Reporte.pdf')
        pdf = open(pdf_dir, "rb")
        return FileResponse(pdf, as_attachment=True)
    else:
        return JsonResponse(data={"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
    

# Return XTF
@api_view(['GET'])
@permission_classes([AllowAny])
def get_log(request: HttpRequest, pk: int):
    try:
        task = Tarea.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse(data={"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if os.path.exists(task.directorio):
        xtf_dir = os.path.join(task.directorio, 'ilivalidator.log')
        xtf = open(xtf_dir, "rb")
        return FileResponse(xtf, as_attachment=True)
    else:
        return JsonResponse(data={"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
