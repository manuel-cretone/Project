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


class Layer(models.Model):

    TYPE_CHOICES = [
    (u'0', u'Convolutional'),
    (u'1', u'Linear'),
    ]

    id = models.AutoField(primary_key=True)
    # type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    input = models.IntegerField()
    output = models.IntegerField()
    kernel = models.IntegerField()
    stride = models.IntegerField()
    padding = models.IntegerField()
    pool_kernel = models.IntegerField()
    pool_stride = models.IntegerField()
    out_dim = models.IntegerField()

    def __str__(self):
        return self.id