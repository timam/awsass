from django.contrib import admin

from .models import Department, Session, Person, Assignment, StudentAssignment


admin.site.register(Department) 
admin.site.register(Session) 
admin.site.register(Person) 
admin.site.register(Assignment) 
admin.site.register(StudentAssignment) 
