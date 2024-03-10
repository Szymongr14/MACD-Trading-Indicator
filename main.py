import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from convert_data import get_data, count_macd, simulate_macd_strategy, simulate_alternative_strategy


UAXUSD_data_frame = get_data('xauusd.csv', 'Gold (ozt) / U.S. Dollar', True)
WIG20_data_frame = get_data('wig20.csv', 'WIG20', False)
count_macd(UAXUSD_data_frame, 'UAX_to_USD', True)
count_macd(WIG20_data_frame, 'WIG20', False)

start_units = 1000
final_capital_WIG20 = simulate_macd_strategy(WIG20_data_frame, start_units)
final_capital_UAXUSD = simulate_macd_strategy(UAXUSD_data_frame, start_units)
print("WIG20 Actions after using MACD: {}%".format(round(final_capital_WIG20 / start_units * 100), 2))
print("UAXUSD Actions after using MACD: {}%".format(round(final_capital_UAXUSD / start_units * 100), 2))
