# Generated by Django 3.2 on 2023-04-22 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamdb', '0011_auto_20230420_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='confirmation_code',
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=150, primary_key=True, serialize=False, unique=True),
        ),
    ]
