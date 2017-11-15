from django.conf.urls import url
from JQ import views

urlpatterns = [
    url(r'^apps/$', views.AppView.as_view(), name='apps'),
    url(r'^apps/(?P<pk>\d+)$', views.AppDetail.as_view() ,name='app_detail'),
    url(r'^company/$', views.CompanyView.as_view(), name='company'),
    url(r'^company/create/$', views.AddCompany.as_view(),name='create_company'),
    url(r'^company/edit/(?P<pk>\d+)$', views.EditCompany.as_view() ,name='edit_company'),
    url(r'^company/delete/(?P<pk>\d+)$', views.DeleteCompany.as_view() ,name='delete_company'),
    url(r'^apps/create/$', views.CreateApp.as_view(), name='create_app'),
    url(r'^apps/edit/(?P<pk>\d+)$', views.EditApp.as_view() ,name='edit_app'),
    url(r'^apps/delete/(?P<pk>\d+)$', views.DeleteApp.as_view() ,name='delete_app'),
    url(r'^apps/dashboard/(?P<pk>\d+)$', views.DashboardView.as_view(), name='dashboard_detail'),
    url(r'^contact/create/$', views.AddContact.as_view(),name='create_contact'),
    url(r'^contact/edit/(?P<pk>\d+)$', views.EditContact.as_view() ,name='edit_contact'),
    url(r'^contact/delete/(?P<pk>\d+)$', views.DeleteContact.as_view() ,name='delete_contact'),
    url(r'^notes/create/$', views.AddNote.as_view(),name='create_note'),
    url(r'^notes/edit/(?P<pk>\d+)$', views.EditNote.as_view() ,name='edit_note'),
    url(r'^notes/delete/(?P<pk>\d+)$', views.DeleteNote.as_view() ,name='delete_note'),
    url(r'^resource/create/$', views.AddResource.as_view(),name='create_resource'),
    url(r'^resource/edit/(?P<pk>\d+)$', views.EditResource.as_view() ,name='edit_resource'),
    url(r'^resource/delete/(?P<pk>\d+)$', views.DeleteResource.as_view() ,name='delete_resource'),
    url(r'^question/$', views.QuestionView.as_view(), name='questions'),
    url(r'^question/create/$', views.AddQuestion.as_view(),name='create_question'),
    url(r'^question/edit/(?P<pk>\d+)$', views.EditQuestion.as_view() ,name='edit_question'),
    url(r'^question/delete/(?P<pk>\d+)$', views.DeleteQuestion.as_view() ,name='delete_question'),
]
