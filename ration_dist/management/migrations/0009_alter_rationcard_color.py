# Generated by Django 4.0.2 on 2022-02-19 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_rename_monthly_income_rationcard_annual_income_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rationcard',
            name='color',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='management.quota'),
        ),
    ]
