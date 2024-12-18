from pydantic import HttpUrl

from app.configs.base import Settings


class DevSettings(Settings):
    # BSC settings
    BSC_RPC_URL: HttpUrl = "https://bsc-testnet.drpc.org"
    BSC_CHAIN_ID: int = 97
