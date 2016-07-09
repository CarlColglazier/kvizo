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
                t, created = Trivia.objects.get_or_create(
                    name = row[0],
                    date = row[1]+"-01-01",
                    category = row[4],
                    subcategory = row[5],
                    is_bonus = False)
                if created:
                    _, created2 = QuestionAndAnswer.objects.get_or_create(
                        parent = t,
                        question_text = row[2],
                        answer = row[3])
                    if created2:
                        continue
                raise CommandError('Something went wrong!')


