# Generated by Django 4.1.2 on 2022-11-09 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_track'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='actual',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='track',
            name='color',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='track',
            name='lastpast',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='track',
            name='orShift',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='track',
            name='plan',
            field=models.CharField(max_length=100),
        ),
    ]
