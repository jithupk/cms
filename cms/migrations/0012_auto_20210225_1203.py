# Generated by Django 3.1.4 on 2021-02-25 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20210225_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='static/images/default.jpg', null=True, upload_to=''),
        ),
    ]
