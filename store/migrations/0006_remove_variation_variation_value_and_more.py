# Generated by Django 5.0.2 on 2024-03-08 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_variation_variation_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='variation_value',
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('4/64', '4/64'), ('8/128', '8/128')], max_length=20),
        ),
    ]
