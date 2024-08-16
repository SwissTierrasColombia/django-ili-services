from django.utils import timezone

from ili_checker_app.models import Tarea
from ili_checker_app.config.enums_config import TaskStatus


def update_task_status(task_id, status):
    task = Tarea.objects.filter(id=task_id)

    task.update(estado=status.value)

    if status in (TaskStatus.COMPLETED, TaskStatus.ERROR):
        task.update(fecha_finalizacion=timezone.now())
