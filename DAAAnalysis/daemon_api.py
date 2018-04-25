import requests
import json

RPC_TEMPLATE = {"jsonrpc": "2.0", "id": "0"}
RPC_HEADERS = {'content-type': 'application/json'}


def get_blockheader_by_height(url, block_height):
    rpc_input = RPC_TEMPLATE
    rpc_input.update({
        "method": "getblockheaderbyheight",
        "params": {"height": block_height}
    })
    response = requests.post(url,
                             data=json.dumps(rpc_input),
                             headers=RPC_HEADERS)
    return response.json()


def get_info(url):
    rpc_input = RPC_TEMPLATE
    rpc_input.update({"method": "get_info"})
    response = requests.post(url,
                             data=json.dumps(rpc_input),
                             headers=RPC_HEADERS)
    return response.json()
