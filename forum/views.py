from django.shortcuts import render
from django.http import HttpResponse

def create_question(request):
	return HttpResponse('create')
def show_question(request):
	return HttpResponse('show')
def questions(request):
	return HttpResponse('questions')