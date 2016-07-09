from django.db import models


class Trivia(models.Model):
    category = models.CharField(max_length=20)
    subcategory = models.CharField(max_length=20)
    name = models.IntegerField()
    date = models.DateField()
    is_bonus = models.BooleanField()

    def __str__(self):
        return str(self.name)

    #def json(self):
        
    def dictionary(self):
        dic = {}
        dic['name'] = self.name
        dic['date'] = self.date.isoformat()
        dic['category'] = self.category
        dic['subcategory'] = self.subcategory
        dic['is_bonus'] = self.is_bonus
        dic['questions'] = []
        for q in QuestionAndAnswer.objects.select_related().filter(parent=self):
            dic['questions'].append(q.dictionary())
        return dic

class QuestionAndAnswer(models.Model):
    parent = models.ForeignKey(Trivia, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=800)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.parent)

    def dictionary(self):
        dic = {}
        dic['text'] = self.question_text
        dic['answer'] = self.answer
        return dic

# TODO
#class Response(models.Model):
