from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = 'core'
urlpatterns = [
    path('', views.record_list, name='record_list'),
    path('export/', views.export_page, name='export_page'),
    path('<int:pk>/', views.record_detail, name='record_detail'),
    path('create/', views.record_create, name='record_create'),
    path('<int:pk>/update/', views.record_update, name='record_update'),
    path('<int:pk>/delete/', views.record_delete, name='record_delete'),
    path('backup/', views.backup_records, name='backup_records'),
    path('restore/', views.restore_records, name='restore_records'),
    path('productivity/', views.admin_productivity, name='admin_productivity'),
    path('productivity/export/', views.export_productivity, name='export_productivity'),
    path('productivity/user/<int:user_id>/', views.user_productivity_details, name='user_productivity_details'),
    path('api/recording-trends/', views.recording_trends, name='recording_trends'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
