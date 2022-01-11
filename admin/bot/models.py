from djongo import models


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Группа: {str(self.name)}'


class User(models.Model):
    _SEX = (('M', 'Male'), ('F', 'Female'))
    telegram_id = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    second_name = models.CharField(max_length=32)
    birth_date = models.DateField(blank=True)
    activated = models.BooleanField(default=False)
    sex = models.CharField(max_length=1, choices=_SEX)
    groups = models.ArrayReferenceField(to=Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.second_name)} {str(self.first_name)}'


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.name} {self.description}'


class Gymnastic(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    value = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.exercise.name} {self.exercise.description} {self.description}. {self.value}'


class Set(models.Model):
    description = models.TextField(blank=True)
    rounds_amount = models.PositiveIntegerField()
    gymnastics = models.ArrayReferenceField(to=Gymnastic, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f' Кол-во раундов: {self.rounds_amount} {self.description} Названия упражнений: <TODO>'
        )


class Training(models.Model):
    description = models.TextField(default=None, blank=True)
    groups = models.ArrayReferenceField(to=Group, on_delete=models.CASCADE)
    sets = models.ArrayReferenceField(to=Set, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=3)
    week_start_date = models.DateField()
    min_rm_percent = models.PositiveIntegerField()
    max_rm_percent = models.PositiveIntegerField()

    def __str__(self):
        return f'Неделя {self.week_start_date}. Тренировка № {self.order}. {self.description} Группы: <TODO>'
