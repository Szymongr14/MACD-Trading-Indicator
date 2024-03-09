import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from convert_data import get_data


def count_macd(df, title):
    # Calculate the 12-period EMA
    df['EMA12'] = df['Closing'].ewm(span=12, adjust=False).mean()
    # Calculate the 26-period EMA
    df['EMA26'] = df['Closing'].ewm(span=26, adjust=False).mean()
    # Calculate MACD (the difference between 12-period EMA and 26-period EMA)
    df['MACD'] = df['EMA12'] - df['EMA26']
    # Calculate the 9-period EMA of MACD (Signal Line)
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    dates = pd.to_datetime(df['Date'])
    prices_averages = df['MACD']
    plt.title('MACD for : ' + title)
    plt.xlabel('Date')
    plt.ylabel('Price Averages')
    plt.plot(dates, df['Signal_Line'], color="red")
    plt.plot(dates, prices_averages)
    plt.show()


UAX_to_USD_graph = get_data('xauusd.csv', 'Gold (ozt) / U.S. Dollar')
WIG20_graph = get_data('wig20.csv', 'WIG20')
count_macd(UAX_to_USD_graph, 'UAX_to_USD')
count_macd(WIG20_graph, 'WIG20')
