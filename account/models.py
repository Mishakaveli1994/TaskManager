from django.core.validators import validate_image_file_extension
from django.db import models
from django.conf import settings
from .validators import validate_image


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
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True,
                              validators=[validate_image])
    position = models.CharField(max_length=12,
                                choices=POSITION_CHOICES,
                                default='employee')

    def __str__(self):
        return f"Profile for user {self.user.username}"
