from tools import collect_daa_data, store_csv_data, separate_by_columns, to_float, \
    read_csv_data, to_int
from plot_builder import plot
from zawy12_stats import LWMA_charts
from config import DAEMON_RPC_URL
import argparse
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def analyze(start_block, end_block, daemon_address=None, csv_file='', read_csv_file=None,
            save_images=False, save_image_path=None, single_image=False, verbose=False):
    print start_block, end_block
    daa_data = []
    if read_csv_file is None:
        url = DAEMON_RPC_URL.format(daemon_address)
        if verbose:
            print "Collecting blockchain data from " + daemon_address + "..."
        daa_data = collect_daa_data(url, start_block, end_block)
        if verbose:
            print "Blockchain data collected!"
        if len(csv_file) > 0:
            if verbose:
                print "Saving data to CSV file..."
            store_csv_data(csv_file, daa_data)
            if verbose:
                print "Data saved!"
    else:
        csv_path = read_csv_file
        if not os.path.isabs(csv_path):
            csv_path = os.path.join(APP_ROOT, csv_path)
        csv_data = read_csv_data(csv_path)
        for csv_row in csv_data:
            daa_data.append(to_float(csv_row))
        daa_data = daa_data[start_block - 1:end_block]
    charts = LWMA_charts(separate_by_columns(daa_data), 120, single_image)
    chart_inx = 0
    chart_paths = []
    filename = os.path.join(APP_ROOT, "charts", "chart_{}.svg")
    if save_image_path is not None:
        filename = os.path.join(save_image_path, "chart_{}.svg")
    for chart in charts:
        if save_images:
            chart_path = filename.format(chart_inx)
            plot(chart['charts'], chart['title'], False, chart_path)
            chart_paths.append(chart_path)
        else:
            plot(chart['charts'], chart['title'], False)
        chart_inx += 1
    return chart_paths


def main():
    parser = argparse.ArgumentParser(description='Difficulty Adjustment Algorithm (DAA) Analysis:')
    parser.add_argument("--start_block", type=int, default=0, required=False,
                        help="Number of block height")
    parser.add_argument("--end_block", type=int, required=False,
                        help="Number of ending block height")
    parser.add_argument("--daemon_address", type=str, required=False,
                        default="localhost:28981", help="ending block height")
    parser.add_argument("--csv_file", type=str, required=False, default='',
                        help="The path to result CSV file.")
    parser.add_argument("--read_csv_data", type=str, required=False,
                        help="The path to the blockchain data CSV file. " +
                             "Note: This option disables collecting data from the blockchain.")
    parser.add_argument("--verbose", action='store_true', required=False, default=False,
                        help="Enable log for script.")
    parser.add_argument("--save_images", action='store_true', required=False, default=False,
                        help="Enable storing of graphics images.")
    args = parser.parse_args()

    start_block = args.start_block
    end_block = start_block + 1
    if args.end_block is not None:
        end_block = args.end_block + 1

    analyze(start_block, end_block, args.daemon_address, args.csv_file, args.read_csv_data,
            args.save_images, verbose=args.verbose)


if __name__ == "__main__":
    main()
