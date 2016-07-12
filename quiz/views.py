from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from quiz.models import Trivia, QuestionAndAnswer, Response
from random import randint
from django.db.models import Count, Q

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

def search_page(request):
    """
    Provides the search page.
    """
    return render(request, 'quizzer/search.html', {})
    
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
    regex = term + r'(?:\W|\p{P}|$)'
    query = QuestionAndAnswer.objects.filter(Q(answer__iregex=regex)|Q(question_text__iregex=regex))
    query = sorted(query, key=lambda x: term.lower() in x.question_text.lower())
    results = [x.parent.dictionary() for x in query]
    return JsonResponse({
        'error': None,
        'result': {
            "items": results
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
    res_all = [x['trivia_id'] for x in Response.objects.values('trivia_id')]
    all = Trivia.objects.filter(pk__in=res_all).values('category').annotate(count=Count('category'))
    res_cor = [x['trivia_id'] for x in Response.objects.filter(points__gt=0).values('trivia_id')]
    cor = Trivia.objects.filter(pk__in=res_cor).values('category').annotate(count=Count('category'))
    correct = {}
    ratios = {}
    totals = {}
    r_list = []
    for o in cor:
        correct[o['category']] = o['count']
    total = 0
    for o in all:
        c = 0
        if o['category'] in correct:
            c = correct[o['category']]
            ratios[o['category']] = 1.0 * correct[o['category']] / o['count']
        else:
            ratios[o['category']] = 0.0
        total += o['count']
        r_list.append({
            "category": o['category'],
            "ratio": ratios[o['category']],
            "correct": c,
            "total": o['count']})
    context = {
        "stats": sorted(r_list, key=lambda x: x['ratio']*(1-x['total']/total)**2, reverse=True)
    }
    print(context)
    return render(request, 'home.html', context)
