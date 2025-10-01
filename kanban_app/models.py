from django.db import models
from django.conf import settings 

class Board(models.Model):

    """
    Represents a project board that contains tasks and members.

    Fields:
    - title: Title of the board
    - owner: User who created/owns the board
    - members: Users who are members of the board

    Properties:
    - member_count: Number of members in the board
    - ticket_count: Total number of tasks in the board
    - tasks_to_do_count: Number of tasks with status 'to-do'
    - tasks_high_prio_count: Number of tasks with priority 'high'
    """
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='boards', blank=True)

    def __str__(self):
        return self.title
    
    @property
    def member_count(self):
        """Return the number of members in this board."""
        return self.members.count()

    @property
    def ticket_count(self):
        """Return the total number of tasks in this board."""
        return self.tasks.count()
    @property
    def tasks_to_do_count(self):
        """Return the number of tasks with status 'to-do'."""
        return self.tasks.filter(status="to-do").count()

    @property
    def tasks_high_prio_count(self):
        """Return the number of tasks with priority 'high'."""
        return self.tasks.filter(priority="high").count()
