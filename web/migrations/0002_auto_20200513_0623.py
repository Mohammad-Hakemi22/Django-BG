# Generated by Django 3.0.6 on 2020-05-13 06:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='images')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], max_length=1)),
            ],
        ),
        migrations.DeleteModel(
            name='test',
        ),
    ]
