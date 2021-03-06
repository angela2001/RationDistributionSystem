# Generated by Django 4.0.2 on 2022-02-19 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_rename_nod_rationcard_no_of_dependants_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rationcard',
            old_name='monthly_income',
            new_name='annual_income',
        ),
        migrations.AddField(
            model_name='rationcard',
            name='eligible_for_AAY',
            field=models.BooleanField(default=False, help_text='Landless laborers, marginal farmers, artisans, crafts men, widows, sick persons, illiterate, disabled adults with no means of subsistence.'),
        ),
    ]
