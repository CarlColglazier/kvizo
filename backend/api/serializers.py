from rest_framework import serializers
from data.models import Tossup, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'answer')

class TossupSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    #category_name = serializers.SerializerMethodField('get_category_display')
    class Meta:
        model = Tossup
        fields = ('category', 'get_category_display', 'difficulty', 'question',)
