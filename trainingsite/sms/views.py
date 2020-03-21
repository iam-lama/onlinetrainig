from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.generic import ListView
from trainboard.models import Student
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#SMS module
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Create your views here.

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

#This decorator marks a view as being exempt from the protection ensured by the middleware 
@csrf_exempt
def sms_response(request):
	resp = MessagingResponse()
	msg = resp.message("Training Site SMS message!")
	return HttpResponse(str(resp))

#This decorator marks a view as being exempt from the protection ensured by the middleware 
@csrf_exempt
def sms_send_message(request, reciever):
	body = "Training Site SMS Message!"
	message = client.messages.create(
        body=body,
        to=reciever,
        from_=settings.TWILIO_NUMBER,
        # status_callback='https://postb.in/1567972985587-6221285020001',
        # status_callback = 'http://localhost:8000/en/sms/send_sms/to/sms_feedback.html'
        )
	
	return render(request, 'sms_feedback.html', {'message':message.status})

class SMSToSendList(LoginRequiredMixin, UserPassesTestMixin, ListView):
	model = Student
	context_object_name = 'students'
	template_name = 'students_list.html'

	def test_func(self):
		return self.request.user.is_superuser

	def dispatch(self, request, *args, **kwargs):
	    user_test_result = self.test_func()
	    if not user_test_result:
	    	# return self.handle_no_permission()
	    	return render(request, '404.html', {'message':'Access to this page is not allowed!!'})
	    return super(UserPassesTestMixin, self).dispatch(request, *args, **kwargs)
