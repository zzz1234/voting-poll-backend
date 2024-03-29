# Generated by Django 5.0 on 2024-01-05 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='votinggame',
            name='game_question',
            field=models.CharField(default='Temp Question?', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
