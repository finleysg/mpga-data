from django.db import models


class ClubManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("golf_course")  # .prefetch_related("contacts")


class ClubContactManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("contact").prefetch_related("roles")


class TeamManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("club")


class MatchPlayResultManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("away_club", "home_club")


class CommitteeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("contact", "home_club")

