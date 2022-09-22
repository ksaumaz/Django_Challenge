# Generated by Django 4.1.1 on 2022-09-22 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IOU', '0003_alter_iou_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[a-zA-Z ]*$', 'Only characters are allowed.')]),
        ),
    ]
