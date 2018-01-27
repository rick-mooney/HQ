from django.conf.urls import url
from tracker import views

urlpatterns = [
    url(r'^task/*?$', views.TaskView.as_view(), name='task'),
    url(r'^task/create/*?$',views.CreateTaskView.as_view(),name='create_task'),
    url(r'^task/confirm_delete/(?P<pk>\d+)$', views.delete_task, name='delete_task'),
    url(r'^task/update/(?P<pk>\d+)$', views.TaskEdit.as_view(), name='update_task'),
    url(r'^task/export/csv/$', views.export_tasks_csv, name='export_tasks_csv'),
    url(r'^project/*?$', views.ProjectView.as_view() ,name='project'),
    url(r'^project/create$', views.CreateProject.as_view(), name='create_project'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectListView.as_view() ,name='project_list'),
    url(r'^project/confirm_delete/(?P<pk>\d+)$', views.ProjectDelete.as_view(), name='delete_project'),
    url(r'^project/update/(?P<pk>\d+)$', views.ProjectEdit.as_view(), name='update_project'),
    url(r'^project/member_delete/(?P<pk>\d+)$', views.DeleteProjectMember.as_view(), name='delete_member'),

    url(r'^canvas/', views.canvas.as_view(), name='canvas'),
     ]
