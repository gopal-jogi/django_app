from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/create/file/', TaskCreateFileView.as_view(), name='task-create-file'),
    path('tasks/create/url/', TaskCreateUrlView.as_view(), name='tasks-create-url'),
    path('tasks/list/', TaskListView.as_view(), name='tasks-list'),
    path('tasks/view/<int:id>/', TaskView.as_view(), name='tasks-view'),
]