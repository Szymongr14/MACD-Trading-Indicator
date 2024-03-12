import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FIGURE_WIDTH = 15


def get_data(file_name, title, day_first):
    df = pd.read_csv(file_name)
    if day_first:
        dates = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    else:
        dates = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    prices = df['Closing']
    plt.figure().set_figwidth(FIGURE_WIDTH)
    plt.title('Historical Rates : ' + title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.plot(dates, prices, color="purple")
    plt.show()
    return df


def count_ema(prices, period):
    alfa = 2 / (period + 1)
    ema = [prices[0]]
    for i in range(1, len(prices)):
        ema.append(prices[i] * alfa + ema[i - 1] * (1 - alfa))
    return ema


def count_macd(df, title, day_first):
    df['EMA12'] = count_ema(df['Closing'], 12)
    df['EMA26'] = count_ema(df['Closing'], 26)
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = count_ema(df['MACD'], 9)

    # TODO save BUY and SELL points and plot it

    for i in range(0, len(df) - 1):
        current_row = df.iloc[i]
        next_row = df.iloc[i + 1]
        if current_row['MACD'] < current_row['Signal_Line'] and next_row['MACD'] > next_row['Signal_Line']:
            df.at[i, 'buy'] = df.at[i, 'MACD']
            df.at[i, 'sell'] = 0
        elif current_row['MACD'] > current_row['Signal_Line'] and next_row['MACD'] < next_row['Signal_Line']:
            df.at[i, 'sell'] = df.at[i, 'MACD']
            df.at[i, 'buy'] = 0
        else:
            df.at[i, 'buy'] = 0
            df.at[i, 'sell'] = 0

    buy_data = df[df['buy'] != 0]
    sell_data = df[df['sell'] != 0]
    buy_points = buy_data['buy']
    sell_points = sell_data['sell']
    if day_first:
        dates_for_sell_points = pd.to_datetime(sell_data['Date'], format='%d/%m/%Y')
        dates_for_buy_points = pd.to_datetime(buy_data['Date'], format='%d/%m/%Y')
        dates = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    else:
        dates_for_sell_points = pd.to_datetime(sell_data['Date'], format='%Y-%m-%d')
        dates_for_buy_points = pd.to_datetime(buy_data['Date'], format='%Y-%m-%d')
        dates = pd.to_datetime(df['Date'])

    prices_averages = df['MACD']
    plt.figure().set_figwidth(FIGURE_WIDTH)
    plt.title('MACD for : ' + title)
    plt.xlabel('Date')
    plt.ylabel('Price Averages')
    plt.plot(dates, df['Signal_Line'], color="red", label='signal line')
    plt.plot(dates, prices_averages, label='MACD')
    plt.scatter(dates_for_buy_points, buy_points, color='green', marker='x', label='buy')
    plt.scatter(dates_for_sell_points, sell_points, color='red', marker='x', label='sell')
    plt.legend()
    plt.show()

    plt.figure().set_figwidth(FIGURE_WIDTH)
    plt.title("BUY and SELL for: " + title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.scatter(dates_for_buy_points, buy_points, color='green', marker='x', label='buy')
    plt.scatter(dates_for_sell_points, sell_points, color='red', marker='x', label='sell')
    plt.plot(dates, df['Closing'], color="purple")
    plt.legend()
    plt.show()


def simulate_macd_strategy(df, start_units):
    actions = start_units
    sold_funds = False

    for i in range(1, len(df)):
        previous_price = df.iloc[i - 1]
        current_price = df.iloc[i]
        if df.at[i, 'buy'] == 1.0 and sold_funds:
            sold_funds = False
            continue

        elif df.at[i, 'sell'] == 1.0 and not sold_funds:
            sold_funds = True
            continue

        if not sold_funds:
            actions = actions * (current_price['Closing'] / previous_price['Closing'])

    return actions


def simulate_alternative_strategy(df, start_units):
    return 1000
