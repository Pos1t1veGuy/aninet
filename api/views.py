from django.shortcuts import render
from django.http import HttpResponse

def get_mail_msgs(request):
	return HttpResponse('mail')
def get_chat_msgs(request):
	return HttpResponse('chat')
def get_videos(request):
	return HttpResponse('videos')