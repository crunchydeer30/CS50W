<<<<<<< HEAD
# Generated by Django 4.1.6 on 2023-02-21 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bid_final_listing_status_alter_bid_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='status',
            new_name='acitve',
        ),
        migrations.AddField(
            model_name='listing',
            name='display_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
=======
# Generated by Django 4.1.6 on 2023-02-21 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bid_final_listing_status_alter_bid_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='status',
            new_name='acitve',
        ),
        migrations.AddField(
            model_name='listing',
            name='display_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
>>>>>>> 55b03087149b060a03fb91d3d02364719933cb76
