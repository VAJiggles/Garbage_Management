# Generated by Django 2.0 on 2018-03-13 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_remove_driver_info_driveraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='days',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('dayValue', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Days',
            },
        ),
        migrations.CreateModel(
            name='schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('address', models.TextField(blank=True, null=True)),
                ('days', models.IntegerField()),
                ('community', models.BooleanField()),
                ('noOfHouses', models.IntegerField(blank=True, null=True)),
                ('specialInst', models.TextField(blank=True, null=True)),
                ('driver_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Schedule',
            },
        ),
        migrations.DeleteModel(
            name='schedule_details',
        ),
        migrations.AlterModelOptions(
            name='garbagedetails',
            options={'verbose_name_plural': 'Garbage Details'},
        ),
        migrations.AlterModelOptions(
            name='user_details',
            options={'verbose_name_plural': 'User Info'},
        ),
        migrations.RenameField(
            model_name='user_details',
            old_name='userId',
            new_name='userType',
        ),
        migrations.RemoveField(
            model_name='garbagedetails',
            name='userDay',
        ),
        migrations.RemoveField(
            model_name='garbagedetails',
            name='userMonth',
        ),
        migrations.RemoveField(
            model_name='garbagedetails',
            name='userYear',
        ),
        migrations.AddField(
            model_name='driver_info',
            name='driver_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.user_details'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='driver_info',
            name='driverLicensePicture',
            field=models.ImageField(default='C:/Users/Deeraj Ramchandani/Desktop/Images/defaultpicture.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='garbagedetails',
            name='garbagePicture',
            field=models.ImageField(default='C:/Users/Deeraj Ramchandani/Desktop/Images/defaultpicture.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='userEmail',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='userProfilePicture',
            field=models.ImageField(default='C:/Users/Deeraj Ramchandani/Desktop/Images/defaultpicture.png', upload_to=''),
        ),
    ]