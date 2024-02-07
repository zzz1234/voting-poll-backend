from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from voting_machine.setup import models
from voting_machine.setup import serializers
from voting_machine.setup.utils import utils


# Create your views here.
class VotingGameList(generics.ListCreateAPIView):
    """List all the games and create games"""

    queryset = models.VotingGame.objects.all()
    serializer_class = serializers.VotingGameSerializer


class VotingGameDetail(generics.RetrieveUpdateDestroyAPIView):
    """Responsible for updating, retrieve or delete a game"""

    queryset = models.VotingGame.objects.all()
    serializer_class = serializers.VotingGameSerializer


class UsersList(generics.ListCreateAPIView):
    """List all the users and create users"""

    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersSerializer


class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    """Responsible for updating, retrieve or delete a users"""

    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersSerializer


class GameUsersList(generics.ListCreateAPIView):
    """List all the game users and create game users"""

    queryset = models.GameUsers.objects.all()
    serializer_class = serializers.GameUsersSerializer


class GameUsersDetail(generics.RetrieveUpdateDestroyAPIView):
    """Responsible for updating, retrieve or delete a game users"""

    queryset = models.GameUsers.objects.all()
    serializer_class = serializers.GameUsersSerializer


class ChoicesList(generics.ListCreateAPIView):
    """List all the choice and create choice"""

    queryset = models.Choices.objects.all()
    serializer_class = serializers.ChoicesSerializer


class ChoicesDetail(generics.RetrieveUpdateDestroyAPIView):
    """Responsible for updating, retrieve or delete a choice"""

    queryset = models.Choices.objects.all()
    serializer_class = serializers.ChoicesSerializer


class VotesList(generics.ListCreateAPIView):
    """List all the votes and create votes"""

    queryset = models.Votes.objects.all()
    serializer_class = serializers.VotesSerializer


class VotesDetail(generics.RetrieveUpdateDestroyAPIView):
    """Responsible for updating, retrieve or delete a votes"""

    queryset = models.Votes.objects.all()
    serializer_class = serializers.VotesSerializer


class CreateNewGame(APIView):
    """Creates a new game"""

    class_serializer = serializers.VotingGameSerializer

    def post(self, request):

        game_name = request.data.get('game_name')
        no_of_votes = request.data.get('no_of_votes')
        game_question = request.data.get('game_question')
        game_code = utils.create_game_code(game_name)
        data = [
            {
                'game_name': game_name,
                'game_code': game_code,
                'game_link': game_code,
                'game_question': game_question,
                'no_of_votes': no_of_votes
            }
        ]

        serializer = self.class_serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Unable to create Game'}
            )


class AddGameUser(APIView):
    """Create a new entry for game user respect to the existing game.
    If the user(email) is already registered, just create mapping of
    existing user with game, else create new user and then create mapping"""

    user_serializer = serializers.UsersSerializer
    user_model = models.Users
    game_user_serializer = serializers.GameUsersSerializer

    def post(self, request):
        user = request.data.get('user_name')
        email = request.data.get('email')
        game_id = request.data.get('game_id')

        valid_users = self.user_model.objects.filter(email=email).values()
        if len(valid_users) == 0:
            user_data = [{'user_name': user, 'email': email}]
            serializer = self.user_serializer(data=user_data, many=True)
            if serializer.is_valid():
                serializer.save()
                user_id = serializer.data[0]['user_id']
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Error while creating User'})
        else:
            user_id = valid_users[0]['user_id']
        game_user_data = [{'game_id': game_id, 'user_id': user_id}]
        serializer = self.game_user_serializer(data=game_user_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Unable to register user to the game'})


class AddChoices(APIView):
    """Add choices to an existing game. Choices are added in bulk"""
    choices_serializer = serializers.ChoicesSerializer

    def post(self, request):
        choices = request.data.get('choices')
        game_id = request.data.get('game_id')
        data = []
        for choice in choices:
            data.append({'game_id': game_id, 'choice_value': choice})
        serializer = self.choices_serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Unable to add choices'})


class GetGameChoices(APIView):
    """Returns the list of choices for a particular game"""

    choices_serializer = serializers.ChoicesSerializer
    choices_model = models.Choices
    voting_game_serializer = serializers.VotingGameSerializer

    def get(self, request, pk):
        # Get game_id from request as pk.
        choices = self.choices_model.objects.filter(game_id__game_id=pk).values()
        return Response(status=status.HTTP_200_OK, data=choices)


class GetGameByGameCode(APIView):
    """Returns the game details for a particular game code"""

    voting_game_serializer = serializers.VotingGameSerializer
    voting_game_model = models.VotingGame

    def get(self, request, game_code):
        # Get game_id from request as pk.
        game = self.voting_game_model.objects.filter(game_code=game_code).values()
        return Response(status=status.HTTP_200_OK, data=game)


class GetUserByEmail(APIView):
    """Returns the user details for a particular user email"""

    users_serializer = serializers.UsersSerializer
    users_model = models.Users

    def get(self, request, email):
        user = self.users_model.objects.filter(email=email).values()
        return Response(status=status.HTTP_200_OK, data=user)


class GetVotesResultsByGameId(APIView):
    """Returns the votes results for a particular game_id"""

    votes_serializer = serializers.VotesSerializer
    votes_model = models.Votes

    def get(self, request, game_id):
        votes = self.votes_model.objects.filter(game_id__game_id=game_id).select_related('choice_id')
        print(votes)
        votes_count = utils.get_votes_count(votes)
        return Response(status=status.HTTP_200_OK, data=votes_count)


class getResultSummaryByGameId(APIView):
    """Returns the result summary for a particular game_id"""

    votes_serializer = serializers.VotesSerializer
    votes_model = models.Votes
    voting_game_serializer = serializers.VotingGameSerializer
    voting_game_model = models.VotingGame

    def get(self, request, game_id):
        votes = self.votes_model.objects.filter(game_id__game_id=game_id).select_related('choice_id')
        game = self.voting_game_model.objects.filter(game_id=game_id).values()
        print(votes)
        summary = utils.get_poll_summary(votes, game)
        # Make changes in API to show choice value instead of choice_id
        vote_response = {'summary': summary}
        return Response(status=status.HTTP_200_OK, data=vote_response)


class getVotesByUserAndGame(APIView):
    """Returns the votes for a particular user_id and game_id"""

    votes_serializer = serializers.VotesSerializer
    votes_model = models.Votes

    def get(self, request, user_id, game_id):
        votes = self.votes_model.objects.filter(game_id__game_id=game_id, user_id__user_id=user_id).values()
        # Make changes in API to show choice value instead of choice_id
        return Response(status=status.HTTP_200_OK, data=votes)


class MyModelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {'message': 'This is a protected endpoint'}
        return Response(status=status.HTTP_200_OK, data=data)


class generateToken(APIView):

    users_serializer = serializers.UsersSerializer
    users_model = models.Users

    def get(self, request):
        # user = self.users_model.objects.get(user_id=user_id)
        token = utils.generate_token(request.user)
        return Response(status=status.HTTP_200_OK, data={'token': token, 'message': 'Token is generated'})
