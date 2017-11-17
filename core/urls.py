from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student_login/$', views.student_login, name='student_loginn'),
    url(r'^student_signup/$', views.student_signup, name='student_signup'),

    url(r'^teacher_login/$', views.teacher_login, name='teacher_login'),
    url(r'^teacher_signup/$', views.teacher_signup, name='teacher_signup'),
]