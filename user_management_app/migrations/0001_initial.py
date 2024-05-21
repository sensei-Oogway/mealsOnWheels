# Generated by Django 4.2.5 on 2024-05-20 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("restaurant_management_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Owner",
            fields=[
                (
                    "email",
                    models.EmailField(
                        default=None,
                        max_length=254,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("password", models.CharField(default=None, max_length=128)),
                (
                    "orders",
                    models.ManyToManyField(
                        blank=True, to="restaurant_management_app.order"
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restaurant_management_app.restaurant",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "email",
                    models.EmailField(
                        default=None,
                        max_length=254,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("password", models.CharField(default=None, max_length=128)),
                ("name", models.CharField(default=None, max_length=100)),
                ("phone", models.CharField(default=None, max_length=15)),
                ("address", models.CharField(default=None, max_length=255)),
                ("location", models.CharField(default=None, max_length=100)),
                (
                    "subscription",
                    models.CharField(
                        choices=[
                            ("monthly", "Monthly"),
                            ("annual", "Annual"),
                            ("no_subscription", "No Subscription"),
                        ],
                        default="no_subscription",
                        max_length=20,
                    ),
                ),
                (
                    "orders",
                    models.ManyToManyField(
                        blank=True, to="restaurant_management_app.order"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Courier",
            fields=[
                (
                    "email",
                    models.EmailField(
                        default=None,
                        max_length=254,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("password", models.CharField(default=None, max_length=128)),
                ("name", models.CharField(default=None, max_length=100)),
                ("phone", models.CharField(default=None, max_length=15)),
                ("vehicle_number", models.CharField(default=None, max_length=20)),
                ("card_details", models.CharField(default=None, max_length=100)),
                ("location", models.CharField(default=None, max_length=100)),
                ("rating", models.FloatField(default=3.5)),
                (
                    "orders",
                    models.ManyToManyField(
                        blank=True, to="restaurant_management_app.order"
                    ),
                ),
            ],
        ),
    ]