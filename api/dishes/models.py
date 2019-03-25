from django.db import models

# Create your models here.
class Dishes(models.Model):
    # dish name 
    name = models.CharField(max_length=255, null=False)
    # name of the restaurant
    restaurant = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.restaurant)