# Generated by Django 3.2.9 on 2021-12-07 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_return_request_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='return',
            name='request_time',
            field=models.TimeField(auto_now=True),
        ),
    ]