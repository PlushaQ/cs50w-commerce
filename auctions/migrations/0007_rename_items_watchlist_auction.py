# Generated by Django 4.1.7 on 2024-02-10 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_watchlist_items_watchlist_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='items',
            new_name='auction',
        ),
    ]
