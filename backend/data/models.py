from django.db import models

DIFFICULTY_LEVELS = (
    ('MS', 'Middle School'),
    ('HS', 'High School'),
    ('College', 'College'),
    ('Open', 'Open'),
    (None, 'None'),
)

CATEGORIES = (
    ('Literature', (
        ('LA', "American Literature"),
        ('LB', "British Literature"),
        ('LE', "European Literature"),
        ('LW', "World Literature"),
        ('LC', "Classical Literature"),
        ('LO', "Other Literature"),
    )),
    ('History', (
        ('HA', "American History"),
        ('HB', "British History"),
        ('HE', "European History"),
        ('HW', "World History"),
        ('HC', "Classical History"),
        ('HO', "Other History"),
    )),
    ('Science', (
        ('SB', "Biology"),
        ('SC', "Chemistry"),
        ('SM', "Math"),
        ('CS', "Computer Science"),
        ('SO', "Other Science"),
    )),
    ('Fine Arts', (
        ('FA', "Auditory Fine Arts"),
        ('FV', "Visual Fine Arts"),
        ('AV', "Audiovisual Fine Arts"),
        ('FO', "Other Fine Arts"),
    )),
    ('Other', (
        ('RL', "Religion"),
        ('PH', "Philosophy"),
        ('MY', "Mythology"),
        ('SS', "Social Science"),
        ('GE', "Geography"),
        ('CE', "Current Events"),
        ('TR', "Trash"),
        (None, 'None'),
    )),
)

class Trivia(models.Model):
    tournament = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    order = models.PositiveSmallIntegerField()
    round = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORIES, null=True)
    difficulty = models.CharField(max_length=7, choices=DIFFICULTY_LEVELS, null=True)
    q_id = models.PositiveIntegerField(unique=True, null=True)
    class Meta:
        abstract = True

class Question(models.Model):
    """
    Represents a single question and answer.
    """
    question = models.TextField()
    answer = models.TextField()

class Tossup(Trivia):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Bonus(Trivia):
    intro_text = models.TextField(blank=True)
    questions = models.ManyToManyField(Question)



