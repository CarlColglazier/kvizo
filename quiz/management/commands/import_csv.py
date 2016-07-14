import csv
from quiz.models import Trivia, QuestionAndAnswer
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Import trivia items from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs=1, type=str)

    def handle(self, *args, **options):
        file = options['file'][0]
        print(file)
        with open(file, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 0
            next(reader) # skip header.
            for row in reader:
                if len(row[3]) > 200 or len(row[2]) < 200 or len(row[2]) < 1 or len(row[3]) < 1:
                    continue
                t, created = Trivia.objects.update_or_create(
                    name = row[0],
                    defaults = {
                        "date": row[1]+"-01-01",
                        "category": row[4],
                        "subcategory": row[5],
                        "level": row[6],
                        "is_bonus": False
                    })
                if not created:
                    first = QuestionAndAnswer.objects.filter(parent=t)[0]
                    if first.question_text != row[2] or first.answer != row[3]:
                        [x.delete() for x in QuestionAndAnswer.objects.filter(parent=t)]
                    else:
                         continue
                c = QuestionAndAnswer.objects.create(
                    parent = t,
                    question_text = row[2],
                    answer = row[3])
                if c:
                    continue
                raise CommandError('Something went wrong!')
