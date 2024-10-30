from aninet.shortcuts import render
from django.http import HttpResponse

def mailbox(request):
	return render(request, 'mailbox.html', {})
def show_message(request, message_id: int):
	return render(request, 'message.html', {})