# backtestbcd-freqtrade
Support backtest num_pair/total_pair once, different timeranges and output !
This script is intended to help overcome weak computers that can backtest many pairs with small time frames (1m) and different timeranges in one run!
User manual:
1) copy to freqtrade folder
2) .source .env/bin/activate
3) python3 backtestbcd.py -n 10 -r "freqtrade backtesting --strategy-list your_stra -c config_test.json --cache none --export signals --timeframe 1m --max-open-trades 3 --enable-protections" --timerange "20220612-20220615 20221108-20221112 20230308-20230312 20230501-"
-n number pair run backtest once on the total number of pairs automatically found in white_pairlist in config_test.json file
-r command to run backtest enclosed in " "
-t times separated by space sign
Future function:
- many different -timeframes
- many different open trades
-.......
