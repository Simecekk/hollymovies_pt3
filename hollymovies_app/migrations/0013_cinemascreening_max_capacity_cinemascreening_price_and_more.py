# Generated by Django 4.2.1 on 2023-06-04 07:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hollymovies_app', '0012_movie_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinemascreening',
            name='max_capacity',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='cinemascreening',
            name='price',
            field=models.FloatField(default=100),
        ),
        migrations.CreateModel(
            name='CinemaTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('screening', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='hollymovies_app.cinemascreening')),
            ],
        ),
    ]