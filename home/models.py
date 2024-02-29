from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    password = models.CharField(max_length=122)

    def __str__(self):
        return self.name


# After creating model in models.py, register it in admin.py and then select the app name from apps.py and paste it in [installed apps under settings.py
# in Hello]
