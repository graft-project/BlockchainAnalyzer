from daemon_api import get_info
import config


def get_mainnet_blockchain_height():
    response = get_info(config.DAEMON_RPC_URL.format(config.LOCAL_DAEMON_ADDRESS_MAINNET))["result"]
    if response["status"] == "OK":
        return response["height"]
    return None
