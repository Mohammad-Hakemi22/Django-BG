# Generated by Django 3.0.7 on 2020-07-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200720_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_author',
            field=models.BooleanField(default=False, verbose_name='نویسنده مقاله'),
        ),
    ]
