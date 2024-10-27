from django.shortcuts import render
from django.http import HttpResponse

def mailbox(request):
	return HttpResponse('mailbox')
def show_message(request):
	return HttpResponse('show_message')