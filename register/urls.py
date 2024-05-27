from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('studentsReg/<int:pk>/', views.studentsReg, name='studentsReg'),
    path('signup/', views.signup, name='signup'),
    path('userLogin/', views.userLogin, name='login'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('detals/<int:pk>/', views.detals, name='detals'),
    path('register_course/<int:course_id>/', views.register_course, name='register_course'),
    path('delete_registration/<int:course_id>/', views.delete_registration, name='delete_registration'),
    path('notifictions/', views.notifictions, name='notifictions'),
    path('', views.redirect_to_login),
]
