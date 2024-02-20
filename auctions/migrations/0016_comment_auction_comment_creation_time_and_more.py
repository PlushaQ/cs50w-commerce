# Generated by Django 4.1.7 on 2024-02-20 20:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='creation_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=500),
        ),
    ]
