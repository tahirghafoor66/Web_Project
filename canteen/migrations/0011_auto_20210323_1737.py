# Generated by Django 3.1.5 on 2021-03-23 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0010_auto_20210323_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='status',
        ),
        migrations.AddField(
            model_name='table',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
