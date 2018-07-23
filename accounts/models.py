from django.db import models

# Create your models here.

class Account(models.Model):
     first_name = models.CharField(max_length=50)
     last_name = models.CharField(max_length=50)
     inn = models.BigIntegerField()
     balance = models.FloatField(default=0.0)

     def __str__(self):
         return self.first_name + ' ' + self.last_name + ' (' + str(self.inn) + ')'

