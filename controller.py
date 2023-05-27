import socket
import pandas as pd
import json
import csv
from game_state import GameState
#from bot import fight
from bot_command import get_move
import sys
from bot import Bot
from buttons import Buttons
from Model import Reading_Data
def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

import csv

def main():
    # Create a CSV file to store the game states
    file = open('game_states.csv', 'w', newline='')
    
    # Create a CSV writer object
    writer = csv.writer(file)
    # Write the header row
    header= ([
        'timer', 'fight_result', 'has_round_started', 'is_round_over',
        'Player1_ID', 'health', 'x_coord', 'y_coord', 'is_jumping', 'is_crouching', 'is_player_in_move', 'move_id',
        'player1_buttons up', 'player1_buttons down', 'player1_buttons right', 'player1_buttons left',
        'Player2_ID', 'Player2 health', 'Player2 x_coord', 'Player2 y_coord', 'Player2 is_jumping', 'Player2 is_crouching',
        'Player2 is_player_in_move', 'Player2 move_id', 'player2_buttons up', 'player2_buttons down',
        'player2_buttons right', 'player2_buttons left'
    ])


    writer.writerow(header)
    


    if (sys.argv[1]=='1'):
        client_socket = connect(9999)
    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)
    current_game_state = None
    bot=Bot()

    

    
    while (current_game_state is None) or (not current_game_state.is_round_over):
        current_game_state = receive(client_socket)
        # print('Received game state:', current_game_state)
        bot_command = bot.fight(current_game_state,sys.argv[1])
        # print('Sending bot command:', bot_command)
        send(client_socket, bot_command)
    # Write the game state to the CSV file
    
        NewRow= ([
            current_game_state.timer,
            current_game_state.fight_result,
            current_game_state.has_round_started,
            current_game_state.is_round_over,
            current_game_state.player1.player_id,
            current_game_state.player1.health,
            current_game_state.player1.x_coord,
            current_game_state.player1.y_coord,
            current_game_state.player1.is_jumping,
            current_game_state.player1.is_crouching,
            current_game_state.player1.is_player_in_move,
            current_game_state.player1.move_id,
            current_game_state.player1.player_buttons.up,
            current_game_state.player1.player_buttons.down,
            current_game_state.player1.player_buttons.right,
            current_game_state.player1.player_buttons.left,
            current_game_state.player2.player_id,
            current_game_state.player2.health,
            current_game_state.player2.x_coord,
            current_game_state.player2.y_coord,
            current_game_state.player2.is_jumping,
            current_game_state.player2.is_crouching,
            current_game_state.player2.is_player_in_move,
            current_game_state.player2.move_id,
            current_game_state.player2.player_buttons.up,
            current_game_state.player2.player_buttons.down,
            current_game_state.player2.player_buttons.right,
            current_game_state.player2.player_buttons.left
        ])

        writer.writerow(NewRow)
        file.flush()

    file.close()
    print('File Written')

    df = pd.read_csv("game_states.csv")
    model = Reading_Data(df)
    bot_command = get_move(current_game_state, model)

    send(client_socket , bot_command)




    
if __name__ == '__main__':
   main()





