import uuid
from tokenize import group

from djongo import models


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f'Группа: {str(self.name)}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class User(models.Model):
    _SEX = (('M', 'Мужской'), ('F', 'Женский'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32, verbose_name='Имя')
    second_name = models.CharField(max_length=32, verbose_name='Фамилия')
    birth_date = models.DateField(blank=True, verbose_name='Дата рождения')
    activated = models.BooleanField(default=False, verbose_name='Активированный')
    sex = models.CharField(max_length=1, choices=_SEX, verbose_name='Пол', blank=True, null=True)
    groups = models.ArrayReferenceField(
        to=Group, on_delete=models.SET_NULL, null=True, verbose_name='Группы'
    )

    def __str__(self):
        return f'{str(self.first_name)} {str(self.second_name)}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Exercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(default=None, blank=True, verbose_name='Описание')
    link = models.URLField(blank=True, verbose_name='Ссылка на видео')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'


class Gymnastic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name='Упражнение')
    description = models.TextField(blank=True, verbose_name='Описание')
    value = models.CharField(max_length=50, blank=False, verbose_name='Повторения')

    def __str__(self):
        return f'{self.exercise.name}: {self.value} повторов'

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class Set(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, verbose_name='Описание')
    rounds_amount = models.PositiveIntegerField(verbose_name='Кол-во раундов')
    gymnastics = models.ArrayReferenceField(
        to=Gymnastic, on_delete=models.CASCADE, verbose_name='Задания'
    )

    def __str__(self):
        ex_names = list(
            Set.objects.filter(id=self.id).values_list('gymnastics__exercise__name', flat=True)
        )
        return f'Упр: {"/".join(ex_names)} Кол-во раундов: {self.rounds_amount}'

    class Meta:
        verbose_name = 'Сет'
        verbose_name_plural = 'Сеты'


class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(default=None, blank=True, verbose_name='Описание')
    groups = models.ArrayReferenceField(
        to=Group, on_delete=models.SET_NULL, verbose_name='Группы', null=True
    )
    sets = models.ArrayReferenceField(to=Set, on_delete=models.CASCADE, verbose_name='Сеты')
    order = models.PositiveIntegerField(default=3, verbose_name='Порядок')
    week_start_date = models.DateField(verbose_name='Дата начала недели')
    min_rm_percent = models.PositiveIntegerField(verbose_name='Мин. процент от макс. веса')
    max_rm_percent = models.PositiveIntegerField(verbose_name='Макс. процент от макс. веса')

    def __str__(self):
        group_names = list(
            Training.objects.filter(id=self.id).values_list('groups__name', flat=True)
        )
        return f'Неделя {self.week_start_date}. Тренировка № {self.order}. Группы: {", ".join(group_names)}'

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
