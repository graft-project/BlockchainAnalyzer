from tools import read_csv_data, separate_by_columns, to_float
from plot_builder import plot
import argparse


def main():
    parser = argparse.ArgumentParser(description='Data Visualization:')
    parser.add_argument("csv_file", type=str, help="The path to the data CSV file.")
    parser.add_argument("--data_titles", type=list, required=False,
                        help="Titles for data sets. Note: If it's empty, script try to read it " +
                             "from first line of CSV file.")
    parser.add_argument("--start", type=int, default=0, required=False,
                        help="Number of start item.")
    parser.add_argument("--end", type=int, required=False,
                        help="Number of start item.")
    parser.add_argument("--verbose", action='store_true', required=False, default=False,
                        help="Enable log for script.")
    parser.add_argument("--output_image", type=str, required=False, default=None,
                        help="Path for output image.")
    args = parser.parse_args()

    origin_data = read_csv_data(args.csv_file)
    titles = args.data_titles
    if titles is None or len(titles) <= 0:
        titles = origin_data[0]
        origin_data.remove(titles)
    data = separate_by_columns(origin_data)
    charts = []
    start = args.start
    end = args.end
    if end is None:
        end = len(data[0])
    for inx in range(1, len(titles), 1):
        charts.append([to_float(data[0][start:end]), to_float(data[inx][start:end]), titles[inx]])
    if args.output_image:
        plot(charts, 'title', False, args.output_image)
    else:
        plot(charts, 'title', False)


if __name__ == "__main__":
    main()
