# Generated by Django 4.1.6 on 2023-02-19 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_category_listing_comments_bid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]