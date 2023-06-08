from django.contrib import admin
from .models import Task



#this class only show the atrr from TaskModel only with readonly_fields 
class TaskAdmin (admin.ModelAdmin):
    readonly_fields = ("created",   )
    

admin.site.register(Task, TaskAdmin)

