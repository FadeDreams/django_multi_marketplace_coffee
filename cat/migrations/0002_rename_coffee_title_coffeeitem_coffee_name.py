# Generated by Django 4.2.6 on 2023-11-02 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coffeeitem',
            old_name='coffee_title',
            new_name='coffee_name',
        ),
    ]
