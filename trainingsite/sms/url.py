from django.urls import path, include
from . import views
from .views import SMSToSendList

urlpatterns = [
	# path('', views.sms_response, name='sms_response'),
    path('send_sms/<reciever>/', views.sms_send_message, name='send_sms'),
    path('sms_list/', SMSToSendList.as_view(), name='sms_list'),

]