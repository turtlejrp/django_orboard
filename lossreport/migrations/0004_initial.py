# Generated by Django 4.1.2 on 2022-12-06 09:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lossreport', '0003_delete_loss'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.CharField(max_length=100)),
                ('lossType', models.CharField(choices=[('Part Supply', 'part_supply'), ('Defect', 'defect'), ('Breakdown', 'breakdown'), ('Short Stop', 'short_stop'), ('Changing/Model Change', 'changing')], max_length=40)),
                ('duration', models.IntegerField(validators=[django.core.validators.MaxValueValidator(1440)])),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]
