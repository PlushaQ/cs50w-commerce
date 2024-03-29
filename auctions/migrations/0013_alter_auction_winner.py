# Generated by Django 4.1.7 on 2024-02-16 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_auction_closed_remove_auction_closed_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='auctions_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
