from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, ModelAdmin
from django.utils import timezone

from .models import Exercise, Group, Gymnastic, Set, Training, User


class AdminSite(admin.AdminSite):
    site_title = "Спорт бот | Панель администратора"
    site_header = "Панель администратора"
    index_title = "Спорт бот | Панель администратора"


class GroupAdmin(ModelAdmin):
    list_display = ('name', 'description')


class ExerciseAdmin(ModelAdmin):
    list_display = ('name', 'description', 'link')


class SetAdmin(ModelAdmin):
    list_filter = (('date_created', DateFieldListFilter),)


class UserAdmin(ModelAdmin):
    list_display = ('__str__', 'group_names', 'sex')
    list_filter = (
        # ('week_start_date', DateFieldListFilter),
        'groups__name',
    )


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('week_start_date', '__str__', 'group_names')
    list_filter = (
        ('week_start_date', DateFieldListFilter),
        'groups__name',
    )

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['sets'].queryset = Set.objects.filter(
            date_created=timezone.datetime.today()
        )
        return super(TrainingAdmin, self).render_change_form(request, context, args, kwargs)


admin_site = AdminSite()
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Exercise, ExerciseAdmin)
admin_site.register(Gymnastic)
admin_site.register(Set, SetAdmin)
admin_site.register(Training, TrainingAdmin)
