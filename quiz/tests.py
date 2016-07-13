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

class QuestionAndAnswerTest(TestCase):
    def setUp(self):
        t = Trivia.objects.create(
            name = "0",
            date = "2000-04-20",
            category = "Trash",
            subcategory = "None",
            is_bonus = False)

    def test_ner(self):
        t = Trivia.objects.get(name="0")
        q = QuestionAndAnswer.objects.create(
            parent = t,
            question_text = """
            The old man feared him and obeyed. Not a word he spoke, but went by
            the shore of the sounding sea and prayed apart to King Apollo whom
            lovely Leto had borne. "Hear me," he cried, "O god of the silver
            bow, that protectest Chryse and holy Cilla and rulest Tenedos with
            thy might, hear me oh thou of Sminthe. If I have ever decked your
            temple with garlands, or burned your thigh-bones in fat of bulls or
            goats, grant my prayer, and let your arrows avenge these my tears
            upon the Danaans."
            """,
            answer = "Answer")
        self.assertEqual(["King Apollo", "Leto", "Chryse", "Cilla", "Tenedos",
                          "Sminthe", "Danaans"],
                         q.named_entities())
            
