# Neural-Network-Trading-Bot

*A work in progress!* 

__Resources used__: Nameko, Numpy, Oanda API, MongoDB, Keras (with Tensorflow backend) 

This is a currency (or other instrument) trading bot using Nameko microservices. It can be used quite easily, with the exception of a possible compatability between Python 3.7 and Nameko. 


# DATA.PY # 

The Oanda API is the first step. It provides the connection to get instrument price. It has a 5000 call limit, which can be make training the neural network tedious. An authentification is required to connect, and after that the API quite simple to use. I used MongoDB as a database to store candle information. We begin with the "Data" class. A nameko @timer decorator is used with the first function **get_ohlc**. This function returns the current hour candle. It has to return two candles because the current 1 hour candle will be incomplete, and we want the last completed candle. I also check to see if there any doubles just in case so that it would not train on the same candlestick if the nameko service was running and set to train on new candlesticks. 

The second function, **get_historical_data**, is nearly identical to the get_ohlc function except that it currently is being used as a call to train the neural network in the next file. It also fetches candlesticks, however, it grabs the past 5000 candles. A neural network won't be useful with 5000 data points. 5000 one hour candles is 208.33 days. The to and from parameters in instruments.InsturmentCandles can specify dates to call candles from Oanda. get_historical_data also saves the candles to MongoDB. Although I currently bypass MongoDB (next file), if the bot were to be used for real trades, it would be advisable to save all the candles to MongoDB and then use the database to train the neural network.

# TRAINER.PY # 

class Trainer also has two functions. The first, **get_model**, handles the neural network model. There you can add more or less nodes or change the neural network as wanted. The input shape is set to 4. The function returns the model. 

The second function, **trainer** preprocesses and cleans the data from the get_historical_data using a nameko proxy, and will then train the model. The data from Oanda is a large JSON, and 'mid' is the key for open, high, low, close price. Afterwards, the data is then put into the ratios: High to low, low to open, close to open, high to low. The neural network will train on these ratios, which really is used to standardize the prices. 

# TO DO # 

Grab enough data to train the neural network, split it, train, and predict! After, the model can be saved and used to visualize or actually execute trades. I will not actually execute the trade (I believe markets are quite efficient), however, a visualization seems like an appropriate next step. 

# Obstacles # 

I was unable to find much documentation on the GreenSSL Socket issue I was having when using the nameko service, so I instead created another Anaconda environment with Python 3.6 where I had to redownload all the necessary packages. That seem to be a quick work around. 
