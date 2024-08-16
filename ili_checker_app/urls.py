from django.urls import path, include
from rest_framework import routers
from ili_checker_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = routers.DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'tareas', views.TareaViewSet)
router.register(r'modelos', views.ModeloViewSet)
router.register(r'regla', views.ReglaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('file/', views.upload_files, name="upload_file"),
    path('get_task_for_user/', views.get_task, name="get_task_for_user"),
    path('get_rules_for_model/<int:pk>/', views.get_rules_for_model, name="get_rules_for_model"),
    path('user_is_admin/', views.user_is_admin, name="user_is_admin"),
    path('get_info_user/', views.get_info_user, name='get_info_user'),
    path('get_report_pdf/<int:pk>/', views.get_pdf, name="get_report_pdf"),
    path('get_report_log/<int:pk>/', views.get_log, name="get_report_xtf"),
]
