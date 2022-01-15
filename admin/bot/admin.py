from django.contrib import admin

from .models import Exercise, Group, Gymnastic, Set, Training, User


class AdminSite(admin.AdminSite):
    site_title = "Спорт бот | Панель администратора"
    site_header = "Панель администратора"
    index_title = "Спорт бот | Панель администратора"


admin_site = AdminSite()


admin_site.register(Group)
admin_site.register(User)
admin_site.register(Exercise)
admin_site.register(Gymnastic)
admin_site.register(Set)
admin_site.register(Training)
