from django.urls import path

from . import views

urlpatterns = [
    path('game', view=views.VotingGameList.as_view(), name='game-view'),
    path('game/<int:pk>', view=views.VotingGameDetail.as_view()),
    path('user', view=views.UsersList.as_view(), name='user-view'),
    path('user/<int:pk>', view=views.UsersDetail.as_view()),
    path('game_user', view=views.GameUsersList.as_view(), name='game-user-view'),
    path('game_user/<int:pk>', view=views.GameUsersDetail.as_view()),
    path('choice', view=views.ChoicesList.as_view(), name='choice-view'),
    path('choice/<int:pk>', view=views.ChoicesDetail.as_view()),
    path('vote', view=views.VotesList.as_view(), name='vote-view'),
    path('vote/<int:pk>', view=views.VotesDetail.as_view()),
    path('create-game', view=views.CreateNewGame().as_view()),
    path('add-game-user', view=views.AddGameUser().as_view()),
    path('add-choice', view=views.AddChoices().as_view()),
    path('game/<int:pk>/choices', view=views.GetGameChoices().as_view()),
    path('game/game-code/<str:game_code>', view=views.GetGameByGameCode().as_view()),
    path('user/user-email/<str:email>', view=views.GetUserByEmail().as_view()),
    path('game/<int:game_id>/results', view=views.GetVotesResultsByGameId().as_view()),
    path('vote/<int:game_id>/user/<int:user_id>', view=views.getVotesByUserAndGame().as_view()),
]
