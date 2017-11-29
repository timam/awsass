from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^student_login/$', views.student_login, name='student_login'),
    url(r'^student_signup/$', views.student_signup, name='student_signup'),
    url(r'^teacher_login/$', views.teacher_login, name='teacher_login'),
    url(r'^teacher_signup/$', views.teacher_signup, name='teacher_signup'),
    url(r'^assignment/$', views.assignment, name='assignment'),
    url(r'^submit_assignment/(?P<alias>[-\w]+)/$', views.submit_assignment, name='submit_assignment'),
    url(r'^assign_assignment/$', views.assign_assignment, name='assign-assignment'),
    url(r'^review_assignemt/(?P<alias>[-\w]+)/$', views.review_assignemt, name='review_assignemt'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]