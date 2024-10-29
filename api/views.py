from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

from AUTH.models import User


def get_mail_msgs(request):
	return HttpResponse('mail')
def get_chat_msgs(request):
	return HttpResponse('chat')
def get_videos(request):
	return HttpResponse('videos')

@csrf_exempt
def post_user_theme(request):
	post_data = json.loads(request.body.decode('utf-8'))
	type = post_data.get('type')
	username = post_data.get('username')
	theme = post_data.get('theme')

	if type == 'set-default-theme':
		if theme in ['dark', 'light', '0', '1']:
			user = get_object_or_404(User, username=username)
			user.is_dark_theme = theme in ['dark', '0']
			user.save()
			return JsonResponse({
				'type': 'request_result',
				'result': 'success',
			})

		return JsonResponse({
			'type': 'request_result',
			'result': 'error',
			'content': 'unknown_theme',
		})
	return JsonResponse({
		'type': 'request_result',
		'result': 'error',
		'content': 'unknown_type',
	})