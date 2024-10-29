from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'home.html', {'user': request.user, 'theme': 'dark' if request.user.is_dark_theme else 'light'})
def animelist(request):
	return HttpResponse('anime')
def anime(request, name: str):
	return HttpResponse(f'anime {name}')
def anime_episode(request, name: str, episode: int):
	return HttpResponse(f'anime {name} episode {episode}')