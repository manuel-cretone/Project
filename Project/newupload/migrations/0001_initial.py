# Generated by Django 2.1.7 on 2019-07-01 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserFiles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('seizureStart', models.IntegerField()),
                ('seizureEnd', models.IntegerField()),
                ('channels', models.IntegerField()),
                ('nSignal', models.IntegerField()),
                ('sampleFrequency', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserNet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=200)),
                ('channels', models.IntegerField()),
                ('windowSec', models.IntegerField()),
                ('sampleFrequency', models.IntegerField()),
            ],
        ),
    ]