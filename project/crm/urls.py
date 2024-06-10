from django.urls import path
from . import views

urlpatterns = [
    path('task/create', views.create_task, name="create_task"),
    path('task/', views.read_tasks, name="read_tasks"),
    path('task/<int:task_id>', views.read_task, name="read_task"),
    path('task/<int:task_id>/get', views.get_task, name="get_task"),
    path('task/<int:task_id>/update', views.update_task, name="update_task"),
    path('task/<int:task_id>/close', views.close_task, name="close_task"),
]