from aninet.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404


def home(request):
	return render(request, 'home.html')
def animelist(request):
	return render(request, 'animelist.html')
def anime(request, name: str):
	return render(request, 'anime.html', {'name': name})
def anime_episode(request, name: str, episode: int):
	anime = get_object_or_404(Anime, name=name)
	episode = anime.get_episode(episode)
	if episode:
		return render(request, 'anime_episode.html', {'anime': anime, 'episode': episode})
	else:
		raise Http404('')