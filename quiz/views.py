from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from quiz.models import Trivia, QuestionAndAnswer, Response
from random import randint
from difflib import SequenceMatcher
from quiz.utils import Search, User

@login_required
def result(request):
    """
    POST requests are sent here after a trivia item is either responded to
    correctly or missed.
    """
    name = request.POST.get("name")
    buzz_point = int(request.POST.get("buzz_points"))
    result = request.POST.get("result")
    trivia = Trivia.objects.get(name=name)
    if trivia.is_bonus:
        if result == "true":
            points =  10
        else:
            points = 0
    else:
        if buzz_point > 0:
            if result == "false":
                points = -5
            else:
                if buzz_point > trivia.questions()[0].bonus_value():
                    points = 20
                else:
                    points = 10
        else:
            if result == "true":
                points = 10
            if result == "false":
                points = 0
    user = request.user
    Response.objects.create(
        trivia = trivia,
        user = user,
        buzz_point = buzz_point,
        points = points)
    #TODO: Handle response on the client.
    return JsonResponse({})

@login_required
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
def search_page(request):
    """
    Provides the search page.
    """
    return render(request, 'quizzer/search.html', {})

@login_required
def search(request):
    """
    Searches the database for corresponding questions and answers.
    """
    if "term" not in request.GET:
        return JsonResponse({
            'error': "No results found",
            'result': None
        })
    term = request.GET.get('term')
    if len(term) < 3:
        return JsonResponse({
            'error': "Query too short",
            'result': None
        })
    if "limit" in request.GET and request.GET.get('limit') == "false":
        limit = 100
    else:
        limit = 25
    c = Search(term, limit)
    return JsonResponse({
        'error': None,
        'result': {
            "items": [x.dictionary() for x in c.results()],
            "entities": c.answer_entities()
        }
    })

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
    user = User(request.user)
    s = user.stats()
    context = {
        "stats": sorted(s['list'], key=lambda x: x['ratio']*(1-x['total']/s['total'])**2, reverse=True)
    }
    return render(request, 'home.html', context)
