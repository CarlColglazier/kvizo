from django.test import TestCase
from quiz.models import Trivia, QuestionAndAnswer

class TriviaTest(TestCase):
    def setUp(self):
        t = Trivia.objects.create(
            name = "0",
            date = "2000-04-20",
            category = "Trash",
            subcategory = "None",
            is_bonus = False)
        QuestionAndAnswer.objects.create(
            parent = t,
            question_text = "Question",
            answer = "Answer")

    def test_question(self):
        t = Trivia.objects.get(name="0")
        self.assertEqual(len(t.questions()), 1)
        q = t.questions()[0]
        self.assertEqual(q.question_text, "Question")
        self.assertEqual(q.answer, "Answer")

    def test_dictionary(self):
        t = Trivia.objects.get(name="0")
        d = t.dictionary()
        self.assertIsNotNone(d)
        self.assertEqual(0, d['name'])
        self.assertEqual("2000-04-20", d['date'])
        self.assertEqual("Trash", d['category'])
        self.assertEqual("None", d['subcategory'])
        self.assertEqual(False, d['is_bonus'])
        self.assertEqual(1, len(d['questions']))
