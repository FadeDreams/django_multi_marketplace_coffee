# Generated by Django 4.2.6 on 2023-11-02 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
        ('cat', '0002_rename_coffee_title_coffeeitem_coffee_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cat',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='cat_name',
            new_name='category_name',
        ),
        migrations.RenameField(
            model_name='coffeeitem',
            old_name='cat',
            new_name='category',
        ),
    ]
