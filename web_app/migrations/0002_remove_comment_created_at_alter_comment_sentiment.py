# Generated by Django 4.2.7 on 2023-11-12 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='comment',
            name='sentiment',
            field=models.CharField(max_length=255),
        ),
    ]