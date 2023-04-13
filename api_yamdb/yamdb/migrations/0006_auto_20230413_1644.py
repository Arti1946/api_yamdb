# Generated by Django 3.2 on 2023-04-13 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("yamdb", "0005_auto_20230413_1639"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genretitle",
            name="genre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="yamdb.genres"
            ),
        ),
        migrations.AlterField(
            model_name="genretitle",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="yamdb.titles"
            ),
        ),
    ]
