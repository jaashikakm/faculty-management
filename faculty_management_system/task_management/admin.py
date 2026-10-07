from django.contrib import admin
from .models import Task, TaskAssignment

admin.site.register(Task)
admin.site.register(TaskAssignment)
