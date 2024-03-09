import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_data(file_name, title):
    df = pd.read_csv(file_name)
    dates = pd.to_datetime(df['Date'])
    prices = df['Closing']
    plt.title('Historical Rates : ' + title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.plot(dates, prices, color="purple")
    plt.show()
    return df
