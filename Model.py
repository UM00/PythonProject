#Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler


def Reading_Data(df):
    #read File
    # df = pd.read_csv("game_states.csv")

    #check coloumns
    for col in df.columns:
        print(f"{col}\n{df[col].head()}\n{df[col].dtype}\n")

    list = [i for i in df.columns if df[i].dtype == 'object' or df[i].dtype == 'bool']

    return Data_Maping(df , list)



def Data_Maping(df , states_data):
    #encoding
    identifiers = {
        'NOT_OVER': 0,
        'P1': 1,
        'P2': 2,
        1: 1,
        0: 0
    }
    for i in states_data:
        df[i]=df[i].map(identifiers)

    for i in df.columns:
        if 'button' in i:
            print(i)
    df = df.dropna()

    X = df.drop(['player1_buttons up','player1_buttons down','player1_buttons right','player1_buttons left','has_round_started','player1_buttons left','player1_buttons right'],axis=1)
    Y = df[['player1_buttons up','player1_buttons down','player1_buttons right','player1_buttons left','has_round_started','player1_buttons left','player1_buttons right']]

    return Model_Training(X, Y)




def Model_Training(X_Cords, Y_Cords):
    #models
    Scaler = MinMaxScaler()

    X_Cords = Scaler.fit_transform(X_Cords)
    train_X,test_X,train_Y,test_Y = train_test_split(X_Cords,Y_Cords,test_size=0.4)

    Regressor = RandomForestRegressor()
    Regressor.fit(train_X, train_Y)

    predicted_Y = Regressor.predict(test_X)
    predicted_Y = np.where(predicted_Y > 0.8,1,0.1)

    predicted_X = Regressor.predict(train_X)
    predicted_X = np.where(predicted_X > 0.8,1,0.1)

    Training_Loss = mean_squared_error(train_Y,predicted_X)
    Testing_Loss = mean_squared_error(test_Y,predicted_Y)

    print("\n")
    print("Training loss is : ", Training_Loss)
    print("Testing loss is : " , Testing_Loss)
    print("\n")

    return predicted_Y













