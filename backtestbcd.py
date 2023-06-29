
"""
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
"""

import json
import os
import glob
import argparse
import subprocess
import logging
import time

logger = logging.getLogger(__name__)

def split_into_chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Parse command line arguments
parser = argparse.ArgumentParser(description='Support backtest num_pair/total_pair once, different timeranges and output !')
parser.add_argument('-n', '--num_pairs', type=int, help='Number of pairs in each command')
parser.add_argument('-r', '--command', type=str, default='python3 backtestbcd.py -n 10 -r "freqtrade backtesting --strategy-list your_stra -c config_test.json --cache none --export signals --timeframe 1m --max-open-trades 3 --enable-protections"', help='Command to execute')
parser.add_argument('-tr', '--timerange', type=str, default="20230310-20230311 20230201-20230202 20220610-20220611 20230102-20230104 20230104-", help='Timerange')

args = parser.parse_args()

start_time = time.time()

if args.command is not None:
    command = args.command
    timerange = args.timerange

    # Split the command string and timerange string into parts
    parts = command.split()
    ranges = timerange.split()

    # Find and extract the value of the '-c' parameter
    config_value = None
    for i in range(len(parts)):
        if parts[i] == '-c' and i + 1 < len(parts):
            config_value = parts[i + 1]
            break

    # Read the content from the config file
    with open(f'{config_value}') as f:
        # Filter out lines starting with '//'
        filtered_lines = [line for line in f if not line.strip().startswith("//")]
        filtered_content = ''.join(filtered_lines)
        data = json.loads(filtered_content)

    pair_whitelist = data['exchange']['pair_whitelist']
    if args.num_pairs is not None and args.num_pairs > 0:
        num_pair_one = args.num_pairs
        pair_test = list(split_into_chunks(pair_whitelist, num_pair_one))
        num_backtest = len(pair_test) * len(ranges)
        print(f"--> OK! Let's run {num_backtest} backtests, please wait....")
        for i, pairs in enumerate(pair_test):
            formatted_pairs = ' '.join(pairs)
            for a, range_str in enumerate(ranges):
                # Construct the backtest command using the command, timerange, and formatted_pairs
                cmd = f"{command} --timerange {range_str} -p {formatted_pairs}"
                print(f"Running command: {cmd}")
                subprocess.run(cmd, shell=True)
    else:
        for a, range_str in enumerate(ranges):
            # Construct the backtest command using the command and timerange
            num_backtest = len(ranges)
            cmd = f"{command} --timerange {range_str}"
            print(f"Running command: {cmd}")
            subprocess.run(cmd, shell=True)

    directory = "user_data/backtest_results/"
    extension = ".json"
    file_list = glob.glob(os.path.join(directory, f"*{extension}"))
    file_list.sort(key=os.path.getmtime, reverse=True)
    filtered_files = [file for file in file_list if "meta" not in os.path.basename(file)]
   
    latest_files = filtered_files[:num_backtest]
    file_names = [f'freqtrade backtesting-show -c {config_value} --export-filename="user_data/backtest_results/{os.path.basename(file)}"' for file in latest_files]
    file_names[-1] = file_names[-1].replace(" &&", "")

    end_time = time.time()

    print(f"\nPrint output: {num_backtest} results\n")
    for name in file_names:
        print(f"Running command: {name}")
        subprocess.run(name, shell=True)
        
    print(f"\n---> Total time taken: {end_time - start_time}")
else:
    print('Error. Example usage: python3 backtestbcd.py -n 5 -r "freqtrade backtesting --strategy-list teststra -c config_test.json --cache none --export signals --timeframe 1m --max-open-trades 1 --enable-protections" --timerange "20230310-20230311 20230201-20230202 20220610-20220611 20230102-20230104 20230104-"')
