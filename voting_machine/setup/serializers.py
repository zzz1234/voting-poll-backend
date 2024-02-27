from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError

from voting_machine.setup import models


class VotingGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VotingGame
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=False)

    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one number")
        if not any(char in "!@#$%^&*()_+-=[]{}|:;<>?,." for char in value):
            raise ValidationError("Password must contain at least one special character")
        return value
    

    def create(self, validated_data):
        user = models.Users.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = models.Users
        fields = '__all__'


class GameUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GameUsers
        fields = '__all__'


class ChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Choices
        fields = '__all__'


class VotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Votes
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=models.Votes.objects.all(),
                fields=('game_id', 'user_id', 'priority'),
                message="Already voted"
            )
        ]
