# Generated by Django 4.1.6 on 2023-02-23 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_bid_price_alter_listing_current_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
