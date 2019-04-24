from nameko.rpc import rpc, RpcProxy
from nameko.timer import timer
from keras.models import Sequential
from keras.layers import Dense
import numpy as np 

decimal_num = 10
class Trainer: 
    name = 'trainer_service'
    
    """  
    This microservice (nameko) takes in the open,high,low,close (ohlc) data from MongoDB to train a neural network 
    """
    y = RpcProxy('data_service')
    
    def get_model(self): 
        model = Sequential()

        model.add(Dense(units=64, activation='relu', input_shape=(4,)))#H2O,L2O,C2O,H2L
        model.add(Dense(units=64, activation='relu'))
        model.add(Dense(units=1, activation='softmax'))
        model.compile(loss='mean_squared_error',
              optimizer='sgd',
              metrics=['accuracy'])
        
        return model 
    
    week = 60*60*24*7

    @timer(interval= week) #this would train the neural network once a week
    def trainer(self):
        
        x =np.ndarray(shape=(0,4))
        y =np.ndarray(shape=(0,1))

        candles = self.y.get_historical_data()['candles']
        previous_close = None
        decimal_num = 10

        for candles in candles:
            candles = candles['mid']   
            candles['o'] = float(candles['o'])
            candles['l'] = float(candles['l'])
            candles['c'] = float(candles['c'])
            candles['h'] = float(candles['h'])
            

            x = np.append(x, np.array([[
            round(candles['h']/candles['o'] - 1, decimal_num), #H2O
            round(candles['l']/candles['o'] - 1, decimal_num), #L2O
            round(candles['c']/candles['o'] - 1, decimal_num), #C2O
            round(candles['h']/candles['l'] - 1, decimal_num)]]), #H2L
            axis=0)                                                 
            
            if previous_close != None: 
                y = np.append(y, np.array([[round(1 - previous_close/ candles['c'], 10) ]]))
            
            previous_close = candles['c'] 

        y = np.append(y, np.array([0])) #needs to be same shape
        

        model = self.get_model()
        fit_model= model.fit(x,y, verbose=True)
        
        print(fit_model)
        print(model)
        print(model.summary) 
           
