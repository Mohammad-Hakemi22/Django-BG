# Generated by Django 3.0.7 on 2020-07-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20200726_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='is_special',
            field=models.BooleanField(default=False, verbose_name='مقاله ویژه'),
        ),
    ]