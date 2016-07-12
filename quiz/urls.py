from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'api/quiz/random/?$', views.random),
    url(r'api/quiz/result/?$', views.result),
    url(r'api/quiz/search', views.search),
    url(r'search/?$', views.search_page, name='search'),
    url(r'^login/?$', login, name='login'),
    url(r'^logout/?$', logout, name='logout'),
    url(r'quizzer/?$', views.quizzer, name='quizzer'),
    url(r'^$', views.index),
]
