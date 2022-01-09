from djongo import models


class User(models.Model):
    SEX = (('M', 'Male'), ('F', 'Female'))
    user_id = models.AutoField(primary_key=True)
    telegram_id = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)
    activated = models.BooleanField(default=False)
    sex = models.CharField(max_length=1, choices=SEX)


class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(max_length=250)

    class Meta:
        abstract = True


class Gymnastic(models.Model):
    gymnastic_id = models.AutoField(primary_key=True)
    exercise = models.EmbeddedField(model_container=Exercise)
    value = models.CharField(max_length=50)


class Set(models.Model):
    set_id = models.AutoField(primary_key=True)
    description = models.CharField(primary_key=50)
    rounds_amount = models.PositiveIntegerField()
    gymnastics = models.ArrayField(model_container=Gymnastic)


class Training(models.Model):
    training_id = models.AutoField(primary_key=True)
    description = models.TextField()
    training_type = models.CharField(max_length=40)
    index = models.PositiveIntegerField()
    week_start_date = models.DateField()
    min_rm_percent = models.PositiveIntegerField()
    max_rm_percent = models.PositiveIntegerField()


class Week(models.Model):
    week_id = models.AutoField(primary_key=True)
    week_start_date = models.DateField()
    trainings = models.ArrayField(model_container=Training)
