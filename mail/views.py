from django.shortcuts import render
from django.http import HttpResponse

def mailbox(request):
	return HttpResponse('mailbox')
def show_message(request, message_id: int):
	return HttpResponse(f'show_message {message_id}')