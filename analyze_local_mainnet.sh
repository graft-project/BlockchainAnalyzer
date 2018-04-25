#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python $DIR/DAAAnalysis/daa_analysis.py \
    --start_block 1 \
    --end_block 69274 \
    --daemon_address 127.0.0.1:18981 \
    --csv_file $DIR/mainnet_blocks.csv \
    --save_images \
    --verbose
