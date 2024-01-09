from datetime import datetime


def create_game_code(game_name):
    now = datetime.now().strftime('%Y%m%d%H%M%S%f')
    unique_game_code = hex(int(now))
    return unique_game_code
