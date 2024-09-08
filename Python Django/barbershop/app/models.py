from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Barber(models.Model):
    fio = models.CharField(max_length=200)
    rank = models.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(6)])
    position=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fio}"

class Shift(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='shifts')
    date = models.DateField()

    def __str__(self):
        return f"{self.date}"

class Client(models.Model):
    name = models.CharField(max_length=200)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    def __str__(self):
        return self.name