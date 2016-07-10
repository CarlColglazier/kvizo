from django.contrib import admin

from .models import Trivia, QuestionAndAnswer, Response

class QuestionAndAnswerInline(admin.StackedInline):
    model = QuestionAndAnswer
    extra = 0

class TriviaAdmin(admin.ModelAdmin):
    """Include attached questions and answers along with the trivia item."""
    inlines = [QuestionAndAnswerInline]
    list_display = ('name','category',)
    search_fields = ('name',)
    
admin.site.register(Trivia, TriviaAdmin)
admin.site.register(Response)
