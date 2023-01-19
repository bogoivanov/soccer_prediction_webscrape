# Generated by Django 4.1.4 on 2023-01-08 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_delete_matchgamefinish_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryFlags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=300)),
                ('country_image', models.ImageField(upload_to='mediafiles/flags/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='matchgameprediction',
            options={'ordering': ['-time_added', 'time']},
        ),
    ]
