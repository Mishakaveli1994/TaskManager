from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    POSITION_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True)
    position = models.CharField(max_length=12,
                                choices=POSITION_CHOICES,
                                default='employee')

    def __str__(self):
        return f"Profile for user {self.user.username}"
