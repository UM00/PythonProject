
from bot import Bot
import numpy as np



def get_move(current_game_state, predicted_values):

    # print(current_game_state)
    # print(predicted_values)


    value = int(np.max(predicted_values))
    # print(value)
    bot = Bot()

    move = bot.fight(current_game_state, value)
    print(move)


    return move