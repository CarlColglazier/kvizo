from quiz.models import Trivia, QuestionAndAnswer
from django.core.management.base import BaseCommand, CommandError
from difflib import SequenceMatcher
import csv

class Command(BaseCommand):
    help = 'Find the most common entries in a category.'

    def add_arguments(self, parser):
        parser.add_argument('category', nargs=1, type=str)
        parser.add_argument('subcategory', nargs=1, type=str)

    def handle(self, *args, **options):
        if "category" not in options or "subcategory" not in options:
            print(help)
            return
        category = options['category'][0]
        subcategory = options['subcategory'][0]
        items = QuestionAndAnswer.objects.filter(
            parent__category=category,
            parent__subcategory=subcategory)
        named = {}
        for i in items:
            answer = i.default_answer()
            if answer in named:
                named[answer] += 1
            else:
                done = False
                for k in named.keys():
                    if SequenceMatcher(None, k, answer).ratio() > 0.75:
                        named[k] += 1
                        done = True
                        break
                if done == False:
                    named[answer] = 1
        #TODO: Also allow the mining of questions.
        """
        for i in items:
            ners = i.named_entities()
            for answer in ners:
                if answer in named:
                    named[answer] += 1
                else:
                    done = False
                    for k in named.keys():
                        if SequenceMatcher(None, k, answer).ratio() > 0.65:
                            named[k] += 1
                            done = True
                            break
                    if done == False:
                        named[answer] = 1
        """
        entities = sorted([x for x in named.items() if x[1] > 0], key=lambda x: x[1], reverse=True)
        entities = [{"term": x[0], "num": x[1]} for x in entities]
        with open(category+"_"+subcategory+"_"+"answers.csv",
                  'w', encoding='utf-8', errors='ignore') as csvfile:
            fields = ["term","num"]
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for i in range(0, len(entities)):
                writer.writerow(entities[i])

            
