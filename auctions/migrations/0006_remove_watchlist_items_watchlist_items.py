# Generated by Django 4.1.7 on 2024-02-10 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_auctions_watchlist_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='items',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='items',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
            preserve_default=False,
        ),
    ]
