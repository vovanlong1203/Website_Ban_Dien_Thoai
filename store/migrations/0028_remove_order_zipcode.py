# Generated by Django 4.1.5 on 2023-04-26 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='zipcode',
        ),
    ]
