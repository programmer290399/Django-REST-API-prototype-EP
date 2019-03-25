from django.db import models

# Create your models here.
class Dishes(models.Model):
    # song title
    name = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    restaurant = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.restaurant)