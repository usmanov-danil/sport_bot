from django.contrib import admin

from .models import Exercise


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = [
        'name',
    ]
    search_fields = ['name']


admin.site.register(Exercise, ExerciseAdmin)
