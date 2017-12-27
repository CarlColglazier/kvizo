from data.models import Tossup, Question
from .serializers import TossupSerializer, QuestionSerializer
from rest_framework import filters, generics, viewsets
from random import sample

class TossupViewSet(viewsets.ModelViewSet):
    queryset = Tossup.objects.all()
    serializer_class = TossupSerializer
    filter_fields = ('category','difficulty',)

class QuestionVS(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('answer',)

class RandomTossupView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TossupSerializer
    filter_fields = ('category','difficulty',)
    def pick_random_object(self):
        # TODO: Make this list depenent on what the user has already seen.
        return sample(
            list(self.filter_queryset(
                Tossup.objects.values_list('pk', flat=True)
            )),
            10)
    def get_queryset(self):
        print(self)
        return Tossup.objects.all().filter(pk__in=self.pick_random_object())
