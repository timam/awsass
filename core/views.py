from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import Person, Assignment, StudentAssignment

from .forms import SignUpForm, CreateAssignmentForm, AssignAssignmentForm
from .enums import PersonGroupType


def index(request):
    return render(request, 'core/index.html',)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.', extra_tags='success')	
    return redirect('/')


#Student Section
@csrf_exempt
def student_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        if not user_id or not password:
            messages.error(request, 'Login failed. please try agin', extra_tags='warning')
            return render(request, 'core/s-log-in.html',
                          {'form': {'non_field_errors': "student id and password must be filled up"}})
        else:
            user = auth.authenticate(user_id=user_id, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.', extra_tags='success')
                    return redirect('dashboard')
            messages.error(request, 'Login failed. please try agin', extra_tags='warning')
            return render(request, 'core/s-log-in.html',
                          {'form': {'non_field_errors': "invalid credential"}})
    return render(request, 'core/s-log-in.html',)

@csrf_exempt
def student_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'core/s-sign-up.html',
                          {'form': form})

        else:
            user_id = form.cleaned_data.get('user_id')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            department = form.cleaned_data.get('department')
            password = form.cleaned_data.get('password')
            person = Person.objects.create_user(user_id=user_id, first_name=first_name, last_name=last_name,
                                       password=password, email=email, department=department,)
            
            person.person_group = PersonGroupType.STUDENT.value
            person.save()
            user = authenticate(user_id=user_id, password=password)
            login(request, user)
            return redirect('/')

    else:
        return render(request, 'core/s-sign-up.html',
                      {'form': SignUpForm()})

#Teacher Section
@csrf_exempt
def teacher_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        if not user_id or not password:
            messages.error(request, 'Login failed. please try agin', extra_tags='warning')
            return render(request, 'core/t-log-in.html',
                          {'form': {'non_field_errors': "user_id and password must be filled up"}})
        else:
            user = auth.authenticate(user_id=user_id, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.', extra_tags='success')
                    return redirect('assignment')
            messages.error(request, 'Login failed. please try agin', extra_tags='warning')
            return render(request, 'core/t-log-in.html',
                          {'form': {'non_field_errors': "invalid credential"}})
    return render(request, 'core/t-log-in.html',)

@csrf_exempt
def teacher_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'core/t-sign-up.html',
                          {'form': form})

        else:
            user_id = form.cleaned_data.get('user_id')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            department = form.cleaned_data.get('department')
            password = form.cleaned_data.get('password')
            person = Person.objects.create_user(user_id=user_id, first_name=first_name, last_name=last_name,
                                                password=password, email=email, department=department,)
            person.person_group = PersonGroupType.TEACHER.value
            person.save()
            user = authenticate(user_id=user_id, password=password)
            login(request, user)
            return redirect('/')

    else:
        return render(request, 'core/t-sign-up.html',
                      {'form': SignUpForm()})

@login_required
def dashboard(request):
    if (request.user.person_group==PersonGroupType.TEACHER.value):
        person_groups= Person.objects.filter(person_group="1")
        return render(request, 'teacher-welcome.html',{'teacher_name':user_name })

    elif(request.user.person_group==PersonGroupType.STUDENT.value):
        student_assignment_list = StudentAssignment.objects.filter(student=request.user.pk)
        return render(request, 'student-welcome.html',{ 'assignments':student_assignment_list})
    

@login_required
def assignment(request):
    if request.user.person_group is not PersonGroupType.TEACHER.value:
        return redirect('/')
    
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if not form.is_valid():
            return render(request, 'assignment.html',
                          {'form': form})

        else:
            teacher = request.user
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')
            session = form.cleaned_data.get('session', None)
            description = form.cleaned_data.get('description', None)
            assignment = Assignment.objects.create(
                teacher=teacher, name=name, department=department,
                session=session, description=description )
            assignment.save()
            messages.error(request, 'An assignment has been created successfully.', extra_tags='success')
            return redirect('assignment')
    
    assignments = Assignment.objects.all().order_by('-created_at')

    return render(request, 'assignment.html', {'form': CreateAssignmentForm(), 'assignments': assignments})   


@login_required
def assign_assignment(request):
    if request.user.person_group is not PersonGroupType.TEACHER.value:
        return redirect('/')
    
    if request.method == 'POST':
        form = AssignAssignmentForm(request.POST, request=request)
        if not form.is_valid():
            return render(request, 'assign-assignment.html',
                          {'form': form})

        else:
            assigned_by = request.user
            assignment = form.cleaned_data.get('assignment')
            student = form.cleaned_data.get('student')
            status = form.cleaned_data.get('status')
            deadline = form.cleaned_data.get('deadline')
            assign_assignment = StudentAssignment.objects.create(
                assigned_by=assigned_by, assignment=assignment, student=student,
                status=status, deadline=deadline)
            assign_assignment.save()
            messages.error(request, 'Assignment has been Assigned to a Student Successfully.', extra_tags='success')
            return redirect('assign-assignment')
    
    assigned_assignments = StudentAssignment.objects.filter(assigned_by=request.user.pk).order_by('-created_at')
    return render(request, 'assign-assignment.html', {'form': AssignAssignmentForm(request=request),
                                                      'assigned_assignments': assigned_assignments})   


def review_assignemt(request):
    teacher_name=request.user.user_id

    return render(request, 'review-assignemt.html')    


@login_required
def submit_addignment(request):
    teacher_name=request.user.user_id

    return render(request, 'submit-addignment.html')   
