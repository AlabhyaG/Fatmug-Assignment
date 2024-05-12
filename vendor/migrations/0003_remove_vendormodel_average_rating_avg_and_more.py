# Generated by Django 5.0.6 on 2024-05-11 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_remove_vendormodel_id_alter_vendormodel_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendormodel',
            name='average_rating_avg',
        ),
        migrations.AddField(
            model_name='vendormodel',
            name='average_response_time',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='vendormodel',
            name='on_time_delivery_rate',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='vendormodel',
            name='quality_rating_avg',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
