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

    for i in range(0, len(df) - 1):
        current_row = df.iloc[i]
        next_row = df.iloc[i + 1]
        if current_row['MACD'] < current_row['Signal_Line'] and next_row['MACD'] > next_row['Signal_Line']:
            df.at[i, 'buy'] = df.at[i, 'Signal_Line']
            df.at[i, 'sell'] = 0
            df.at[i, 'buy_price'] = df.at[i, 'Closing']
            df.at[i, 'sell_price'] = 0
        elif current_row['MACD'] > current_row['Signal_Line'] and next_row['MACD'] < next_row['Signal_Line']:
            df.at[i, 'sell'] = df.at[i, 'Signal_Line']
            df.at[i, 'buy'] = 0
            df.at[i, 'sell_price'] = df.at[i, 'Closing']
            df.at[i, 'buy_price'] = 0
        else:
            df.at[i, 'buy'] = 0
            df.at[i, 'sell'] = 0
            df.at[i, 'buy_price'] = 0
            df.at[i, 'sell_price'] = 0

    buy_data = df[df['buy'] != 0]
    sell_data = df[df['sell'] != 0]
    buy_price_data = df[df['buy_price'] != 0]
    sell_price_data = df[df['sell_price'] != 0]
    buy_points = buy_data['buy']
    sell_points = sell_data['sell']
    buy_price = buy_price_data['buy_price']
    sell_price = sell_price_data['sell_price']
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
    plt.scatter(dates_for_buy_points, buy_points, color='green', marker='^', label='buy', zorder=2)
    plt.scatter(dates_for_sell_points, sell_points, color='red', marker='v', label='sell', zorder=2)
    plt.legend()
    plt.show()

    plt.figure().set_figwidth(FIGURE_WIDTH)
    plt.title("BUY and SELL for: " + title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.scatter(dates_for_buy_points, buy_price, color='green', marker='^', label='buy', zorder=2)
    plt.scatter(dates_for_sell_points, sell_price, color='red', marker='v', label='sell', zorder=2)
    plt.plot(dates, df['Closing'], zorder=1)
    plt.legend()
    plt.show()


def simulate_macd_strategy(df, start_units):
    actions_are_sold = False
    buy_price = 0
    balance = start_units

    for i in range(1, len(df) - 1):
        current_price = df.iloc[i]
        if current_price['buy_price'] != 0.0 and actions_are_sold:
            # print("bought: {}".format(df.at[i, 'buy_price']))
            buy_price = df.at[i, 'buy_price']
            actions_are_sold = False
            continue

        elif current_price['sell_price'] != 0.0 and not actions_are_sold:
            # print("sold: {} {}".format(df.at[i, 'sell_price'], i))
            sell_price = df.at[i, 'sell_price']
            actions_are_sold = True
            diff = sell_price - buy_price
            balance += diff
            # print("diff: {}".format(diff))
            continue

    return balance


def simulate_alternative_strategy(df, start_units, cooldown_period=3):
    holding = False
    buy_price = 0
    balance = start_units
    cooldown_count = 0

    for i in range(1, len(df) - 1):
        current_price = df.iloc[i]
        if current_price['buy_price'] != 0.0 and cooldown_count == 0:
            cooldown_count = cooldown_period
            buy_price = df.at[i, 'buy_price']
            holding = False
            continue

        elif current_price['sell_price'] != 0.0 and not holding:
            sell_price = df.at[i, 'sell_price']
            holding = True
            diff = sell_price - buy_price
            balance += diff
            continue

        if cooldown_count > 0:
            cooldown_count -= 1

    return balance
