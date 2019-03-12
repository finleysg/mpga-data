from django.db import models
from django.db.models.aggregates import Count
from random import randint


class PhotoManager(models.Manager):

    def random(self, tournament, year):
        count = self.filter(year=year).filter(tournament=tournament).aggregate(count=Count("id"))["count"]
        random_index = randint(0, count - 1)
        return self.filter(year=year).filter(tournament=tournament)[random_index]

    def available_years(self, tournament):
        return self.filter(tournament=tournament).order_by().values_list("year").distinct()
