from django.db import models

class Worker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    citizenship = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company}"
