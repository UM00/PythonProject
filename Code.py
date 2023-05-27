import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler
import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
warnings.filterwarnings("ignore")

df = pd.read_excel("TRUE_FILE.xls").drop('Unnamed: 0',axis=1)


for i in df.columns:
    print(i)
    print(df[i].head())
    print(df[i].dtype,'\n')


    catagorical = []
for i in df.columns:
    if df[i].dtype == 'object' or df[i].dtype == 'bool':
        catagorical.append(i)

keys = {'NOT_OVER': 0,
       'P1':1,
       'P2':2,
       True:1,
       False:0
       }


for i in catagorical:
    df[i]=df[i].map(keys)



for i in df.columns:
    if 'button' in i:
        print(i)


df = df.dropna()

X = df.drop(['player1_button_up','player1_button_down','player1_button_right','player1_button_left','player1_button_select','player1_button_start','player1_button_Y','player1_button_B','player1_button_X','player1_button_A','player1_button_L','player1_button_R'],axis=1)
Y = df[['player1_button_up','player1_button_down','player1_button_right','player1_button_left','player1_button_select','player1_button_start','player1_button_Y','player1_button_B','player1_button_X','player1_button_A','player1_button_L','player1_button_R']]


X.isna().sum()

sc = StandardScaler()
rb = RobustScaler()
X = sc.fit_transform(X)
X = rb.fit_transform(X)


x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)

print(y_train.shape)


reg = LinearRegression()
reg.fit(x_train, y_train)
y_pred = reg.predict(x_test)
y_pred = np.where(y_pred > 0.5,1,0)
print(f"loss is {mean_squared_error(y_test,y_pred)}")


print(y_pred[0])

with open('Model.pkl', 'wb') as f:
    pickle.dump(reg, f)