from django.contrib import admin

from .models import *


admin.site.register(Task)
admin.site.register(User)
admin.site.register(ExamSheet)
admin.site.register(Answer)
admin.site.register(Solution)
