#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python $DIR/DAAAnalysis/update_block_data.py $DIR/mainnet_blocks.csv \
    --daemon_address 127.0.0.1:18981
