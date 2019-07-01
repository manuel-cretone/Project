from django.db import models

# Create your models here.
class UserNet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    # file = models.FileField(upload_to='usermodels')
    link = models.CharField(max_length = 200)
    channels = models.IntegerField()
    windowSec = models.IntegerField()
    sampleFrequency = models.IntegerField()

    def __str__(self):
        return self.name

class UserFiles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    seizureStart = models.IntegerField()
    seizureEnd = models.IntegerField()
    channels = models.IntegerField()
    nSignal = models.IntegerField()
    sampleFrequency = models.IntegerField()

    def __str__(self):
        return self.name