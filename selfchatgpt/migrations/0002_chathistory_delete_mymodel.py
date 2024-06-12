# Generated by Django 5.0.6 on 2024-06-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("selfchatgpt", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_question", models.TextField()),
                ("system_response", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name="MyModel",
        ),
    ]