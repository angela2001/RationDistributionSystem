# Generated by Django 4.0.2 on 2022-02-19 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_rename_price_kerosine_in_l_quota_price_kerosine_per_l_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rationcard',
            name='nod',
            field=models.IntegerField(default=0),
        ),
    ]
