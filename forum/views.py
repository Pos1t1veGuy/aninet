from django.shortcuts import render
from django.http import HttpResponse

def create_question(request):
	return HttpResponse('create')
def show_question(request, question_id: int):
	return HttpResponse(f'show {question_id}')
def questions(request):
	return HttpResponse('questions')