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
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(User,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='opened_tasks')

    assignee = models.ForeignKey(User,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='taken_tasks')

    status = models.CharField(max_length=12,
                              choices=STATUS_CHOICES,
                              default='opened')

    priority = models.CharField(max_length=10,
                                choices=PRIORITY_CHOICES,
                                default='low')

    estimate = models.FloatField(default=0)

    parent_task = models.ForeignKey('self', null=True, blank=True,
                                    default=None, on_delete=models.CASCADE)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
