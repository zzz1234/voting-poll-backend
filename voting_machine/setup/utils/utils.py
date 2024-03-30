import openai
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from voting_machine.setup import models
from voting_machine.setup.utils import secret_utils
# import pandas as pd


def get_completion(prompt, model="gpt-3.5-turbo"):
    openai.api_key = secret_utils.get_secret('OpenAIApiKey')
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def create_game_code(game_name):
    now = datetime.now().strftime('%Y%m%d%H%M%S%f')
    unique_game_code = hex(int(now))
    return unique_game_code


def get_votes_count(votes):
    votes_count = {}
    total_number_of_votes = votes[0].game_id.no_of_votes
    for vote in votes:
        # Append vote data
        if vote.choice_id.choice_value not in votes_count:
            votes_count[vote.choice_id.choice_value] = 0
        votes_count[vote.choice_id.choice_value] += total_number_of_votes + 1 - vote.priority
    ret_data = []
    for key, value in votes_count.items():
        ret_data.append({'name': key, 'value': value})
    return ret_data


def get_poll_summary(votes, game):
    vote_dict = fetch_vote_data(votes)
    prompt = f"""
    We have a dataset of a poll "{game[0]['game_question']}", understand the context of the poll from the question, choice and comments.
    Generate a summary of the poll defining who the winner was, what was the reason(try to understand from the comments). Mention if there was any close second or a tie or any different scenario.
    The summary should include below information in below format(enclose the content in <p> tag and use HTML tags to render the result):
    Winner of the poll(in bold):
    Reason: Write a very brief summary in less than 50 words from the comments corresponding to the winner of the poll.
    Close second: Write a very brief summary in less than 50 words from the comments corresponding to the close second of the poll.
    Find the dataset enclosed in backticks below:
    ```
    {vote_dict}
    ```
    """
    response = get_completion(prompt)
    return response


def fetch_vote_data(votes):
    vote_dict = []
    for vote in votes:
        temp = {}
        temp['vote_id'] = vote.vote_id
        temp['choice'] = vote.choice_id.choice_value
        temp['comments'] = vote.comments
        vote_dict.append(temp)
    return vote_dict


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def authenticate(email, password):
    try:
        user = models.Users.objects.get(email=email)
        if user.password == password:
            return user
        else:
            return None
    except models.Users.DoesNotExist:
        return None


def get_base_url(request):
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    return f'{protocol}://{current_site.domain}'
