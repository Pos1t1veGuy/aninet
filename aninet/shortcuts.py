from django.shortcuts import render as django_render
from django.http import HttpResponse

def render(request, template_path: str, kwargs: dict = {}) -> HttpResponse:
	return django_render(request, template_path, {
		'user': request.user,
		'theme': ('dark' if request.user.is_dark_theme else 'light') if request.user.is_authenticated else 'dark',
		**kwargs,
	})
