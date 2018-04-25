from tools import collect_daa_data
from config import DAEMON_RPC_URL
from daemon_api import get_info
import argparse
import csv
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def update_block_data(data_file, daemon_address):
    url = DAEMON_RPC_URL.format(daemon_address)
    csv_path = data_file
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(APP_ROOT, csv_path)
    first_block = 1
    with open(csv_path, 'r') as f:
        last_line = f.readlines()[-1]
        first_block = int(last_line.split(',')[0]) + 1
        f.close()
    last_block = 0
    response = get_info(url)['result']
    if response["status"] == "OK":
        last_block = response["height"]
    block_data = collect_daa_data(url, first_block, last_block)
    with open(csv_path, 'a') as f:
        writer = csv.writer(f)
        for data_row in block_data:
            writer.writerow(data_row)


def main():
    parser = argparse.ArgumentParser(description='Blockchain Update Script:')
    parser.add_argument("data_file", type=str, help="Path to blockchain data file.")
    parser.add_argument("--verbose", action='store_true', required=False, default=False,
                        help="Enable log for script.")
    parser.add_argument("--daemon_address", type=str, required=False, default="localhost:28981",
                        help="ending block height")
    args = parser.parse_args()
    update_block_data(args.data_file, args.daemon_address)


if __name__ == "__main__":
    main()
