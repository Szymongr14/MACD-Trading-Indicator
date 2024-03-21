from convert_data import get_data, count_macd, simulate_macd_strategy, simulate_alternative_strategy

UAXUSD_data_frame = get_data('data/xauusd.csv', 'Gold (ozt) / U.S. Dollar', True)
KGHM_data_frame = get_data('data/kgh_d.csv', 'KGHM SA', False)
count_macd(UAXUSD_data_frame, 'UAX_to_USD', True)
count_macd(KGHM_data_frame, 'KGHM SA', False)

start_units = 1000
final_capital_KGHM = simulate_macd_strategy(KGHM_data_frame, start_units)
final_capital_UAXUSD = simulate_macd_strategy(UAXUSD_data_frame, start_units)
final_alternative_capital_KGHM = simulate_alternative_strategy(KGHM_data_frame, start_units)
final_alternative_capital_UAXUSD = simulate_alternative_strategy(UAXUSD_data_frame, start_units)
print("----------------RESULTS----------------\nStart units: {}zł\n".format(start_units))

print("After using MACD indicator:")
print("Final units KGHM SA: {}zł ({}%)".format(round(final_capital_KGHM, 2),round(final_capital_KGHM / start_units * 100) - 100, 2))
print("Final units UAXUSD: {}zł ({}%)".format(round(final_capital_UAXUSD, 2),round(final_capital_UAXUSD / start_units * 100) - 100, 2))


print("\nAfter using alternative strategy:")
print("Final units KGHM SA: {}zł ({}%)".format(round(final_alternative_capital_KGHM, 2),round(final_alternative_capital_KGHM / start_units * 100) - 100, 2))
print("Final units UAXUSD: {}zł ({}%)".format(round(final_alternative_capital_UAXUSD, 2),round(final_alternative_capital_UAXUSD / start_units * 100) - 100, 2))
