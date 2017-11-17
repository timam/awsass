from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .models import Person, Assignment, StudentAssignment


def index(request):
    return render(request, 'index.html',)


#Student Section
def student_login(request):
    return render(request, 's-log-in.html',)

def student_signup(request):
    return render(request, 's-sign-up.html',)

#Teacher Section
def teacher_login(request):
    return render(request, 't-log-in.html',)

def teacher_signup(request):
    return render(request, 't-sign-up.html',)
