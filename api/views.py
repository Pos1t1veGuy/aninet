from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from AUTH.models import User


def get_mail_msgs(request):
	return HttpResponse('mail')
def get_chat_msgs(request):
	return HttpResponse('chat')
def get_videos(request):
	return HttpResponse('videos')

def post_user_theme(request):
	type = request.POST.get('type')
	username = request.POST.get('username')
	theme = request.POST.get('theme')

	if type == 'set-default-theme':
		if theme in ['dark', 'light', '0', '1']:
			theme = theme in ['dark', '0']
			user = get_object_or_404(User, username=username)
			user.is_dark_theme = theme
			user.save()