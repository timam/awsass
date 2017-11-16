from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .models import Person, Assignment, StudentAssignment


def index(request):
    return render(request, 'index.html',)
