from django.db import models


class Trivia(models.Model):
    """
    Trivia models a trivia item such as a tossup or bonus.
    """
    category = models.CharField(max_length=20)
    subcategory = models.CharField(max_length=20)
    name = models.IntegerField()
    date = models.DateField()
    is_bonus = models.BooleanField()

    def __str__(self):
        return str(self.name)

    def questions(self):
        """Get the questions attached to the object."""
        return QuestionAndAnswer.objects.select_related().filter(parent=self)
        
    def dictionary(self):
        """Returns the Trivia model as a dictionary."""
        dic = {}
        dic['name'] = self.name
        dic['date'] = self.date.isoformat()
        dic['category'] = self.category
        dic['subcategory'] = self.subcategory
        dic['is_bonus'] = self.is_bonus
        dic['questions'] = []
        for q in self.questions():
            dic['questions'].append(q.dictionary())
        return dic

class QuestionAndAnswer(models.Model):
    """
    QuestionAndAnswer models a trivia item with a single question and a single
    answer. This is useful for storing both questions and answers for
    tossups (where there is a single question and answer) and bonuses
    (where there are multiple questions and answers).
    """
    parent = models.ForeignKey(Trivia, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=800)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.parent)

    def dictionary(self):
        """Returns the QuestionAndAnswer model as a dictionary."""
        dic = {}
        dic['text'] = self.question_text
        dic['answer'] = self.answer
        return dic

# TODO
#class Response(models.Model):
