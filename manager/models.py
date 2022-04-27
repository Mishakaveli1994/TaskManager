from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = (
        ('opened', 'Opened'),
        ('in_progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed')
    )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )

    RESOLUTION_CHOICES = (
        ('unresolved', 'Unresolved'),
        ('resolved', 'Resolved'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(User,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='opened_tasks')

    assignee = models.ForeignKey(User,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='taken_tasks')

    status = models.CharField(max_length=12,
                              choices=STATUS_CHOICES,
                              default='opened')

    priority = models.CharField(max_length=10,
                                choices=PRIORITY_CHOICES,
                                default='low')

    estimate = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])

    parent_task = models.ForeignKey('self', null=True, blank=True,
                                    default=None, on_delete=models.CASCADE)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tracked_time = models.IntegerField(null=True, blank=True, default=0)

    resolved = models.CharField(max_length=10,
                                choices=RESOLUTION_CHOICES,
                                default='unresolved')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class TimeEntry(models.Model):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.assignee.username} tracked {self.time}H on task {self.parent_task}"


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activityMessage = models.CharField(max_length=200)
    project = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.user.username} has {self.activityMessage}"
