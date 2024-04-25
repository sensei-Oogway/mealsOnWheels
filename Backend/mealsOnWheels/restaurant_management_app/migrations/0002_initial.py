# Generated by Django 4.2.5 on 2024-04-25 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management_app', '0001_initial'),
        ('restaurant_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_requests',
            field=models.ManyToManyField(to='user_management_app.courier'),
        ),
        migrations.AddField(
            model_name='order',
            name='menu',
            field=models.ManyToManyField(to='restaurant_management_app.menuitem'),
        ),
    ]