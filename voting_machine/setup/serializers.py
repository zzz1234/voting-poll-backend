from rest_framework import serializers

from voting_machine.setup import models


class VotingGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VotingGame
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):

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
