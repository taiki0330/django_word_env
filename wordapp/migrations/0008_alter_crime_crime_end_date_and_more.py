# Generated by Django 4.1 on 2024-03-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordapp', '0007_alter_crime_crime_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crime',
            name='crime_end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='crime',
            name='crime_start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='crime',
            name='suspect_birthday',
            field=models.DateField(null=True),
        ),
    ]