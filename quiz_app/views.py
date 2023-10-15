from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView

from quiz_app.api import ApiClient
from quiz_app.game import Quiz


# Create your views here.

def index(request):
    try:
        quiz = ApiClient.get_quiz_options()
        return render(request, 'index.html', quiz)
    except ValueError:
        return render(request, 'quiz_app/error.html')


def start_game(request):
    number_of_questions = request.POST['quantity']
    difficulty = request.POST['difficulty']
    category = request.POST['category']
    quiz = Quiz.create_game(number_of_questions, difficulty, category)
    quiz.save(request)
    return redirect('/on_game')


def on_game(request):
    quiz = Quiz.restore(request)
    if not quiz:
        return render(request, 'quiz_app/error.html')

    answer = request.POST.get('answer')
    try:
        if answer:
            quiz.check_answer(answer)

        question = quiz.get_question()
        quiz.save(request)
        return render(request, 'quiz_app/game.html', vars(question))
    except IndexError as x:
        return redirect('/finish')


def finish(request):
    quiz = Quiz.restore(request)
    result = quiz.get_result()
    quiz.stop(request)
    return render(request, 'quiz_app/finish.html', result)


@cache_page(60 * 15)
def my_view(request):
    data = Quiz.get_result
    context = {
        'data': data,
    }
    return render(request, 'quiz_app/game.html')


def ranking_view(request, Quiz):
    quiz = Quiz.get_result
    duration = quiz.end_time - quiz.start_time

    context = {
        'quiz': quiz,
        'duration': duration
    }
    return render(request, 'ranking_template.html', context)
