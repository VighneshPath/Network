# Generated by Django 3.0.6 on 2020-07-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20200714_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_stamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
