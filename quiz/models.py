from django.db import models
from django.contrib.auth.models import User
import string

table = str.maketrans(string.punctuation, "                                ")

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

    def words(self):
        """Number of words in the question. Used to determine buzz time."""
        return len(self.question_text.split(" "))

    def bonus_value(self):
        words = self.question_text.split(" ")
        index = words.index("(*)") if "(*)" in words else -1
        return self.words() - index

    def named_entities(self):
        """
        Produces an array of named entities (i.e. people, battles, books) from
        the question text. This is a rather naive algorithm which uses the
        capitalization of works in the question to extract groups of capitalized
        words. Since questions tend to have very similar formatting, this method
        has good results in most cases.
        """
        phrases = []
        phrase_words = ["of","at","the","v", "is", "to", "a", "an", "on", "de",
                        "la", "from", "da", "el", "for", "by", "as", "that"]
        banned = ["I"]
        words = self.question_text.split()
        current = None
        for i in range(1, len(words)):
            word = words[i].translate(table).strip()
            if len(word) < 1:
                    continue
            if current == None:
                if word[0].isupper() and not '.' in words[i-1] and not ',' in words[i-1]:
                    current = word
            else:
                if (word[0].isupper() or word in phrase_words) and (len(words[i-1]) < 5 or ('.' not in words[i-1] and ',' not in words[i-1])):
                    current += " " + word
                else:
                    if current not in banned:
                        c = current.split()
                        while c[-1] in phrase_words:
                            c.pop()
                        if len(c) > 0:
                            phrases.append(" ".join(c))
                    current = None
        if current is not None:
            if current not in banned:
                c = current.split()
                while c[-1] in phrase_words:
                    c.pop()
                    phrases.append(" ".join(c))
                if len(c) > 0:
                    phrases.append(current)
        return phrases


class Response(models.Model):
    """
    A Response is logged whenever a Trivia item is reviewed.
    """
    trivia=models.ForeignKey(Trivia, on_delete=models.CASCADE)
    user=models.ForeignKey(User)
    points=models.SmallIntegerField(default=0)
    buzz_point=models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
