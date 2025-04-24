from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('project/', views.index, name='Index'),
    path('project/list/', views.ProjectListView.as_view(), name='ProjectsList'),
    path('project/create/', views.ProjectCreateView.as_view(), name='ProjectCreate'),
    path('project/update/<int:pk>', views.ProjectUpdateView.as_view(), name='ProjectUpdate'),
    path('project/delete/<int:pk>', views.ProjectDeleteView.as_view(), name='ProjectDelete'),
    path('task/create', views.TaskCreateView.as_view(), name='TaskCreate'),
    path('task/update/<int:pk>', views.TaskUpdateView.as_view(), name='TaskUpdate'),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name='TaskDelete'),
]

