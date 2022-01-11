from django.contrib import admin

from .models import Exercise, Group, Gymnastic, Set, Training, User

admin.site.register(User)
admin.site.register(Training)
admin.site.register(Group)
admin.site.register(Set)
admin.site.register(Exercise)
admin.site.register(Gymnastic)
