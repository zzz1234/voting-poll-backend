from django.db import models


# Create your models here.
class VotingGame(models.Model):
    """To initialize a Game Setup"""
    game_id = models.AutoField(primary_key=True)
    game_code = models.CharField(max_length=30, unique=True, blank=False)  # Needs to be generated via some encoding algo to make sure its unique.
    game_name = models.CharField(max_length=50, blank=False)
    game_question = models.CharField(max_length=500, blank=False)
    game_link = models.CharField(max_length=100, blank=False)  # Not sure if we should keep this as we can remove it later and keep URL as concatentation of a HTTP string and game_code.
    no_of_votes = models.PositiveIntegerField(blank=False)


class Users(models.Model):
    """Properties of a User"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=False)


class GameUsers(models.Model):
    """Mapping of Users with GameID"""
    game_user_id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(VotingGame, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


class Choices(models.Model):
    """Represents choices for a game"""
    choice_id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(VotingGame, on_delete=models.CASCADE, db_column='game_id')
    choice_value = models.CharField(max_length=200)


class Votes(models.Model):
    """Votes given by Users"""
    vote_id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(VotingGame, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Choices, on_delete=models.CASCADE)
    priority = models.IntegerField()
    comments = models.CharField(max_length=500)
