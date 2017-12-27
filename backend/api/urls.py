from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views

router = routers.DefaultRouter()
router.register(r'tossups', views.TossupViewSet)
router.register(r'questions', views.QuestionVS)
router.register(r'random', views.RandomTossupView, base_name='rand-tossups')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^obtain-auth-token/$', obtain_auth_token)
]
