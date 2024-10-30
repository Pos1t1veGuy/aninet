from aninet.shortcuts import render
from django.http import HttpResponse

def create_question(request):
	return render(request, 'create_question.html', {})
def show_question(request, question_id: int):
	return render(request, 'show_question.html', {})
def questions(request):
	return render(request, 'questions.html', {})