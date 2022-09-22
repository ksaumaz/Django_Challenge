# Generated by Django 4.1.1 on 2022-09-22 06:21

import IOU.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='IOU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[IOU.models.validate_iou_amount])),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrower', to='IOU.user')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lender', to='IOU.user')),
            ],
        ),
    ]
