# Generated by Django 5.0.6 on 2024-05-11 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0002_remove_purchaseordermodel_delivered_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseordermodel',
            name='delivery_date',
        ),
        migrations.AlterField(
            model_name='purchaseordermodel',
            name='order_date',
            field=models.DateTimeField(),
        ),
    ]
