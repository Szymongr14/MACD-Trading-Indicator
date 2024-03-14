from convert_data import get_data, count_macd, simulate_macd_strategy, simulate_alternative_strategy

# older dates first !
UAXUSD_data_frame = get_data('xauusd.csv', 'Gold (ozt) / U.S. Dollar', True)
LPP_data_frame = get_data('cdr_d.csv', 'LPP SA', False)
count_macd(UAXUSD_data_frame, 'UAX_to_USD', True)
count_macd(LPP_data_frame, 'LPP SA', False)

start_units = 1000
final_capital_LPP = simulate_macd_strategy(LPP_data_frame, start_units)
final_capital_UAXUSD = simulate_macd_strategy(UAXUSD_data_frame, start_units)
final_alternative_capital_LPP = simulate_alternative_strategy(LPP_data_frame, start_units)
final_alternative_capital_UAXUSD = simulate_alternative_strategy(UAXUSD_data_frame, start_units)
print("----------------RESULTS----------------\nStart units: 1000zł")


print("LPP SA actions after using MACD: \n{}%".format(round(final_capital_LPP / start_units * 100) - 100, 2))
print("Final units: {}zł".format(round(final_capital_LPP, 2)))


print("UAXUSD actions after using MACD: {}%".format(round(final_capital_UAXUSD / start_units * 100)- 100, 2))
print("LPP SA actions after using MACD based strategy: {}%".format(round(final_alternative_capital_LPP / start_units * 100)- 100, 2))
print("UAXUSD actions after using MACD based strategy: {}%".format(round(final_alternative_capital_UAXUSD / start_units * 100) -100, 2))
