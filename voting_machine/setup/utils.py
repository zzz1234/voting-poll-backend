from datetime import datetime
# import pandas as pd


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
