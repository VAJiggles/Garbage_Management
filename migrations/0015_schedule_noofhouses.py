# Generated by Django 2.0 on 2018-03-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_remove_schedule_noofhouses'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='noOfHouses',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]