# Generated by Django 5.0 on 2024-01-05 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0002_votinggame_game_question_alter_users_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choices',
            name='game_id',
            field=models.ForeignKey(db_column='game_id', on_delete=django.db.models.deletion.CASCADE, to='setup.votinggame'),
        ),
    ]
