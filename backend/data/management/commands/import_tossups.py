from django.core.management.base import BaseCommand, CommandError
from data.models import *
import pandas as pd
from ftfy import fix_encoding
from html.parser import HTMLParser

h = HTMLParser()

def process_text(s):
    return h.unescape(
        fix_encoding(s)
    ).replace('\\\'', '\'').replace('\\\"', '\"').replace('";', '"').replace('\r\n', '')

class Command(BaseCommand):
    help = "Import tossups from a CSV"

    def add_arguments(self, parser):
        parser.add_argument("file", nargs=1, type=str)

    def handle(self, *args, **option):
        if len(option['file']):
            choices=Tossup._meta.get_field("category").choices
            ch = {element[1]:element[0] for tupl in [x[1] for x in choices] for element in tupl}
        
            for file in option['file']:
                try:
                    data = pd.read_csv(file, thousands=',').fillna('')
                    data_dict = data.to_dict(orient='records')
                    tossups = []
                    for record in data_dict:
                        if not record['Question'] or not record['Answer'] or not record['Category'] or not record['Difficulty']:
                            continue
                        q = Question(
                            question=process_text(record['Question']),
                            answer=process_text(record['Answer'])
                        )
                        q.save()
                        if record['Category'] in ['Literature', 'History', 'Fine Arts', 'Science']:
                            if not record['Subcategory']:
                                record['Subcategory'] = "Other"
                            if record['Category'] is "Science":
                                if record['Subcategory'] == "Other":
                                    category = "Other Science"
                                else:
                                    category = record['Subcategory']
                            else:
                                category = ' '.join(
                                    [record['Subcategory'], record['Category']]
                                )
                        else:
                            category = record['Category']
                        if category in ch:
                            category = ch[category]
                        else:
                            category = None
                        if not record['Difficulty']:
                            record['Difficulty'] = None
                        t = Tossup(
                            tournament=record['Tournament'],
                            year=record['Year'],
                            order=record['Question #'],
                            round=record['Round'],
                            category=category,
                            difficulty=record['Difficulty'],
                            q_id=record['ID'],
                            question=q
                        )
                        tossups.append(t)
                    Tossup.objects.bulk_create(tossups)
                except Exception as e:
                    print("Could not process {}".format(file))
                    print(e)
