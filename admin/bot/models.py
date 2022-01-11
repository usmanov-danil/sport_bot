from djongo import models


class Group(models.Model):
    _id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Группа: {str(self.name)}'


class User(models.Model):
    _SEX = (('M', 'Male'), ('F', 'Female'))
    _id = models.ObjectIdField()
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
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=None, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.name}. {self.description}.'

    class Meta:
        abstract = True


class Gymnastic(models.Model):
    _id = models.ObjectIdField()
    exercise = models.ArrayReferenceField(to=Exercise, on_delete=models.CASCADE)
    value = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'{self.exercise.name}. {self.exercise.description}. {self.value}'

    class Meta:
        abstract = True


class Set(models.Model):
    _id = models.ObjectIdField()
    description = models.CharField(max_length=50)
    rounds_amount = models.PositiveIntegerField()
    gymnastics = models.ArrayField(model_container=Gymnastic)

    def __str__(self):
        return f'{self.description}. Кол-во раундов: {self.rounds_amount}'

    class Meta:
        abstract = True


class Training(models.Model):
    _id = models.ObjectIdField()
    description = models.TextField(default=None, blank=True)
    groups = models.ArrayReferenceField(to=Group, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    week_start_date = models.DateField()
    min_rm_percent = models.PositiveIntegerField()
    max_rm_percent = models.PositiveIntegerField()

    def __str__(self):
        return f'Неделя {self.week_start_date}. Тренировка № {self.order}. {self.description}'
