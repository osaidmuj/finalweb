from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('studentsReg/<int:pk>/', views.studentsReg, name='studentsReg'),
    path('signup/', views.signup, name='signup'),
    path('userLogin/', views.userLogin, name='login'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('view/<int:pk>/', views.view, name='view'),
    path('register_course/<int:course_id>/', views.register_course, name='register_course'),
    path('delete_registration/<int:course_id>/', views.delete_registration, name='delete_registration'),
    path('news/', views.news, name='news'),
    path('', views.redirect_to_login),
]
