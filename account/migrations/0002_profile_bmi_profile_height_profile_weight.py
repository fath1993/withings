# Generated by Django 5.0.2 on 2024-05-28 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bmi',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='bmi'),
        ),
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='height'),
        ),
        migrations.AddField(
            model_name='profile',
            name='weight',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='weight'),
        ),
    ]
