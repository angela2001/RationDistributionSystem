# Generated by Django 4.0.2 on 2022-02-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_alter_rationcard_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rationcard',
            name='card_no',
            field=models.CharField(default='0000000000', editable=False, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
