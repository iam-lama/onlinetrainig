from django.urls import path, include
from . import views
from django.views.generic import ListView
from .views import HomePageView,CourseDetailView

urlpatterns = [
    path('', HomePageView.as_view(template_name='index.html'), name='index'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course_apply/<int:pk>', views.course_apply, name='course_apply'),
    path('payment/',views.payment,name='payment')
]