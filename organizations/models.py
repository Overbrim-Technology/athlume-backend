from django.conf import settings
from django.db import models

# Create your models here.
class Organization(models.Model):
    # Link to the admin account for this specific org/school
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    logo = models.ImageField(upload_to='org_logos/', blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class School(Organization):
    principal_name = models.CharField(max_length=100)
    established_year = models.IntegerField()

    def __str__(self):
        return f"{self.name} (Established: {self.established_year})"