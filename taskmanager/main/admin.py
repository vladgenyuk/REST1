from django.contrib import admin
from .models import Task, SubTask, SubTaskTaskRelations


class STaskAdmin(admin.ModelAdmin):
    list_display = ("task", 'subtask', 'char', 'bool', 'bool2', 'time' )
    fields = ("task", 'subtask', 'char', 'bool', 'bool2', 'time' )


admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(SubTaskTaskRelations, STaskAdmin)