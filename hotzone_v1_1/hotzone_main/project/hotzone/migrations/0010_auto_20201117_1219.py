# Generated by Django 3.1.2 on 2020-11-17 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotzone', '0009_auto_20201117_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationdetail',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
