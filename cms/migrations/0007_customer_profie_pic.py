# Generated by Django 3.1.4 on 2021-02-24 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profie_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
