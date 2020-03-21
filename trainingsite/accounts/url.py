from django.urls import path, include
from .views import accounts, students, tutors
from django.contrib.auth import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', accounts.SignUpView.as_view(), name='signup'),
    path('signup/student/', students.StudentSignUpView.as_view(), name='student-signup'),
    path('signup/tutor/', tutors.TutorSignUpView.as_view(), name='tutor-signup' ),
    path('edit/student/<int:pk>/', students.StudentEditView.as_view(), name='student-edit'),
    path('my_account/', TemplateView.as_view(template_name='profile.html'), name='profile'),
]
