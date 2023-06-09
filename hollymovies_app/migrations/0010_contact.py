# Generated by Django 4.2.1 on 2023-05-28 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hollymovies_app', '0009_alter_comment_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('priority', models.IntegerField()),
            ],
        ),
    ]
