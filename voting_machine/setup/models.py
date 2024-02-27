from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class VotingGame(models.Model):
    """To initialize a Game Setup"""
    game_id = models.AutoField(primary_key=True)
    game_code = models.CharField(max_length=30, unique=True, blank=False)  # Needs to be generated via some encoding algo to make sure its unique.
    game_name = models.CharField(max_length=50, blank=False)
    game_question = models.CharField(max_length=500, blank=False)
    game_link = models.CharField(max_length=100, blank=False)  # Not sure if we should keep this as we can remove it later and keep URL as concatentation of a HTTP string and game_code.
    no_of_votes = models.PositiveIntegerField(blank=False)



class UsersManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    """Properties of a User"""
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UsersManager()

    USERNAME_FIELD = 'email'


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
