from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    token = models.TextField(blank=True, null=True)
    answer = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email