from django.db import models

# Create your models here.
class UserNet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    file = models.FileField(upload_to='usermodels')
    link = models.CharField(max_length = 200)
    channels = models.CharField(max_length=10)
    windowSize = models.CharField(max_length=20)

def __str__(self):
    return self.model_name
