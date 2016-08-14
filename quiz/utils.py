from quiz.models import Trivia, QuestionAndAnswer, Response
from itertools import chain
from difflib import SequenceMatcher
from django.db.models import Count

class Search():
    """
    Search is a helper class that queries the database.
    """
    term = ""
    answers = []
    questions = []

    def __init__(self, term, limit):
        self.term = term
        self.regex = self.term + r'(?:\y)'
        self.answers = Trivia.objects.filter(questionandanswer__answer__iregex=self.regex)[:limit]
        self.questions = Trivia.objects.filter(questionandanswer__question_text__iregex=self.regex)[:limit]

    def answer_entities(self):
        named = {}
        entities = [x.questionandanswer_set.all()[0].named_entities() for x in list(self.answers)]
        for en in entities:
            for e in en:
                if e in named:
                    named[e] += 1
                else:
                    done = False
                    for k in named.keys():
                        if SequenceMatcher(None, k, e).ratio() > 0.65:
                            named[k] += 1
                            done = True
                            break
                    if done == False:
                        named[e] = 0
        entities = sorted([x for x in named.items() if x[1] > 0], key=lambda x: x[1], reverse=True)
        entities = [{"term": x[0], "num": x[1]} for x in entities]
        return entities

    def results(self):
        return list(chain(self.answers, self.questions))

class User():

    user = None
    
    def __init__(self, user):
        """
        Initializes the User.
        """
        print(user)
        self.user = user

    def all_responses(self):
        return Trivia.objects.filter(response__user=self.user)

    def correct_responses(self):
        return Trivia.objects.filter(response__user=self.user, response__points__gt=0)

    def stats(self):
        """
        Currently used for the table on the homepage.
        """
        all = self.all_responses().values('category').annotate(count=Count('category'))
        cor = self.correct_responses().values('category').annotate(count=Count('category'))
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
        return {
            'list': r_list,
            'total': total
        }
