from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^student_login/$', views.student_login, name='student_login'),
    url(r'^student_signup/$', views.student_signup, name='student_signup'),
    url(r'^create_asignment/$', views.create_asignment, name='create_asignment'),
    url(r'^teacher_login/$', views.teacher_login, name='teacher_login'),
    url(r'^assignment/$', views.assignment, name='assignment'),
    url(r'^submit_addignment/$', views.submit_addignment, name='submit_addignment'),
    url(r'^assign_assignment/$', views.assign_assignment, name='assign_assignment'),
    url(r'^review_assignemt/$', views.review_assignemt, name='review_assignemt'),
    url(r'^teacher_signup/$', views.teacher_signup, name='teacher_signup'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]