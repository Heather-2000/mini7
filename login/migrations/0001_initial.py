# Generated by Django 5.0.6 on 2024-06-12 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("pw", models.CharField(max_length=1000)),
            ],
        ),
    ]