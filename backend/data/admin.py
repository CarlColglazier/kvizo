from django.contrib import admin

from .models import Tossup, Bonus, Question

admin.site.register(Tossup)
admin.site.register(Bonus)
admin.site.register(Question)
