from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from quiz.models import Trivia, QuestionAndAnswer
from random import randint

def result(request):
    """
    POST requests are sent here after a trivia item is either responded to
    correctly or missed.
    """
    # TODO: Process results.
    name = request.POST.get("name")
    trivia = Trivia.objects.get(name=name)
    print(trivia.name, request.user)
    return JsonResponse({})

def random(request):
    """
    Responds with a randomly selected trivia item.
    """
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory') or "All"
    if category is None or category == "All":
        random_idx = randint(0, Trivia.objects.count() - 1)
        random_obj = Trivia.objects.all()[random_idx]
    else:
        if subcategory == "All":
            filtered = Trivia.objects.filter(category=category)
        else:
            filtered = Trivia.objects.filter(category=category, subcategory=subcategory)
        count = filtered.count()
        if count < 1:
            return JsonResponse({'error': 'No results.',
                                 'result': None})
        random_idx = randint(0, count - 1)
        random_obj = filtered[random_idx]
    return JsonResponse({'error':None,
                         'result':random_obj.dictionary()})

@login_required
def quizzer(request):
    """
    Responds with an HTML page for the quizzer program.
    """
    context = {}
    return render(request, 'quizzer/quizzer.html', context)

def index(request):
    """
    Home page.
    """
    context = {}
    return render(request, 'base.html', context)
