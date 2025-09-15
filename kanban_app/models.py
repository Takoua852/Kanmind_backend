from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owned_boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='boards', blank=True)

    def __str__(self):
        return self.title
    
    @property
    def member_count(self):
        return self.members.count()

    @property
    def ticket_count(self):
        return 0  # TODO: falls du später ein Task-Modell hast

    @property
    def tasks_to_do_count(self):
        return 0

    @property
    def tasks_high_prio_count(self):
        return 0
