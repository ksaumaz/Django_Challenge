# Generated by Django 4.1.1 on 2022-09-22 14:05

import IOU.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IOU', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iou',
            name='amount',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=10, validators=[IOU.models.validate_iou_amount]),
        ),
    ]
