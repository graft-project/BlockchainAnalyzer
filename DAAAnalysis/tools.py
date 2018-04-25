from daemon_api import get_blockheader_by_height
import csv


def collect_daa_data(url, start_block, end_block):
    daa_data = []
    for block in range(start_block, end_block):
        result = get_blockheader_by_height(url, block)["result"]
        print block
        if result["status"] == "OK":
            block_header = result["block_header"]
            daa_data.append([block_header["height"],
                             block_header["timestamp"],
                             block_header["difficulty"]])
    return daa_data


def store_csv_data(filepath, data):
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        for data_row in data:
            writer.writerow(data_row)


def read_csv_data(filepath):
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for data_row in reader:
            data.append(data_row)
    return data


def separate_by_columns(data):
    separated = []
    if len(data) > 0:
        for row_elm in data[0]:
            separated.append([])
        for data_row in data:
            for inx, elm in enumerate(data_row):
                separated[inx].append(elm)
    return separated


def to_float(data):
    return [float(i) for i in data]


def to_int(data):
    return [int(i) for i in data]
