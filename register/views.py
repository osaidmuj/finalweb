from django.shortcuts import render, redirect, get_object_or_404
from .forms import createNewUser
from .models import Courses, Students, StudentsReg, News
from .filters import CourseFilter
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages

@login_required(login_url='login')
def courses(request):
    courses = Courses.objects.all()
    searchFilter = CourseFilter(request.POST, queryset=courses)
    courses = searchFilter.qs
    context = {
        'courses': courses,
        'searchFilter': searchFilter,
    }
    return render(request, "register/courses.html", context)




@login_required(login_url='login')
def studentsReg(request, pk):
    student = get_object_or_404(Students, id=pk)
    registrations = StudentsReg.objects.filter(studentId=pk)
    courses = []
    for reg in registrations:
        course = reg.courseId
        if course and course.scheduleId:
            courses.append({
                'name': course.name,
                'description': course.description,
                'instructor': course.instructor,
                'roomNo': course.scheduleId.roomNo,
                'days': ', '.join([day.name for day in course.scheduleId.days.all()]),
                'startTime': course.scheduleId.startTime.strftime('%H:%M'),
                'endTime': course.scheduleId.endTime.strftime('%H:%M')
            })
    context = {
        'student_name': student,
        'courses': courses
    }
    return render(request, 'register/studentsReg.html', context)

def signup(request):
    form = createNewUser()
    if request.method == 'POST':
        form = createNewUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  
            user.save()
            Students.objects.create(user=user)   
            return redirect('login')
    return render(request, 'register/create.html', {'form': form})

def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('courses')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'register/login.html')



@login_required
def register_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    student = request.user.student

    storage = get_messages(request)
    list(storage)  

    if StudentsReg.objects.filter(studentId=student, courseId=course).exists():
        messages.warning(request, 'You are already registered for this course.')
    else:
        
        student_courses = StudentsReg.objects.filter(studentId=student)
        for reg in student_courses:
            if reg.courseId.scheduleId and course.scheduleId:
                if reg.courseId.scheduleId.days.filter(id__in=course.scheduleId.days.all()).exists() and (
                        (reg.courseId.scheduleId.startTime <= course.scheduleId.startTime <= reg.courseId.scheduleId.endTime) or
                        (reg.courseId.scheduleId.startTime <= course.scheduleId.endTime <= reg.courseId.scheduleId.endTime)):
                    messages.error(request, 'There is a schedule conflict with another course.')
                    return redirect('view', pk=course_id)

        StudentsReg.objects.create(courseId=course, studentId=student)
        messages.success(request, 'You have successfully registered for the course.')

    return redirect('view', pk=course_id)

@login_required
def delete_registration(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    student = request.user.student

    storage = get_messages(request)
    list(storage) 

    registration = StudentsReg.objects.filter(courseId=course, studentId=student)
    if registration.exists():
        registration.delete()
        messages.success(request, 'You have successfully deleted the course registration.')
    else:
        messages.error(request, 'You are not registered for this course.')

    return redirect('view', pk=course_id)

@login_required(login_url='login')
def userLogout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')

def news(request):
    news = News.objects.all()
    return render(request, 'register/news.html', {'news': news})

@login_required(login_url='login')
def view(request, pk):
    course = get_object_or_404(Courses, id=pk)
    studentReg = StudentsReg.objects.filter(courseId=course).count()
    is_registered = StudentsReg.objects.filter(courseId=course, studentId=request.user.student).exists()
    return render(request, 'register/view.html', {
        'course': course,
        'studentReg': studentReg,
        'is_registered': is_registered
    })

def redirect_to_login(request):
    return redirect('login')
