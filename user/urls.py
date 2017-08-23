from django.conf.urls import url
from user import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)

urlpatterns = [
    url(r'^home/$', views.home,name='home'),
    url(r'^about/$',views.about,name='about'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^signup/$', views.signup,name='signup'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/change-password/$', views.change_password, name='change_password'),

    url(r'^reset-password/$', password_reset, {'template_name':'password_reset_form.html',
    'post_reset_redirect': 'user:password_reset_done',
    'email_template_name': 'password_reset_email.html'}, name='reset_password'),

    url(r'^reset-password/done/$', password_reset_done,
    {'template_name': 'password_reset_done.html'}, name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    password_reset_confirm, {'template_name': 'password_reset_confirm.html',
    'post_reset_redirect':'user:password_reset_complete'}, name='password_reset_confirm'),

    url(r'^reset-password/complete/$', password_reset_complete,
    {'template_name':'password_reset_complete.html'}),
    # Run email server for debugging
    # python -m smtpd -n -c DebuggingServer localhost:1025
    ]
