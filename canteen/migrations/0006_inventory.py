# Generated by Django 3.1.5 on 2021-03-14 06:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0005_auto_20210314_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=3)),
                ('qty', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canteen.dish')),
            ],
        ),
    ]