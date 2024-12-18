from decimal import Decimal

from web3 import AsyncWeb3
from bip_utils import Bip44, Bip44Coins
from bip_utils.bip.bip44_base.bip44_base import Bip44Changes
from eth_account import Account

from app.configs import settings
from app.schemas.wallet import GeneratedWalletFullData


class BSC_Client:
    CHAIN_ID = settings.BSC_CHAIN_ID

    def __init__(self):
        self.w3 = AsyncWeb3(provider=AsyncWeb3.AsyncHTTPProvider(endpoint_uri=str(settings.BSC_RPC_URL)))

    async def generate_wallet(self, index: int = 0) -> GeneratedWalletFullData:
        """
        Generate a wallet address and keys from a master private key using BIP-44.

        Args:
            index (int): The index for the derived address (default is 0).

        Returns:
            GeneratedWalletFullData: Wallet containing address, private key, and public key.
        """
        master_account = Account.from_key(settings.MASTER_PRIVATE_KEY)

        bip44_mst_ctx = Bip44.FromPrivateKey(master_account.key, Bip44Coins.ETHEREUM)
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_INT).AddressIndex(index)

        derived_private_key = bip44_acc_ctx.PrivateKey().Raw().ToHex()
        derived_address = bip44_acc_ctx.PublicKey().ToAddress()
        derived_public_key = bip44_acc_ctx.PublicKey().RawCompressed().ToHex()

        return GeneratedWalletFullData(
            address=derived_address,
            private_key=derived_private_key,
            public_key=derived_public_key,
        )

    async def balance_check(self, private_key: str) -> Decimal:
        """
        Check the balance of a wallet address.

        Args:
            private_key (str): The private key of the wallet address.

        Returns:
            Decimal: The balance of the wallet address.
        """
        balance_wei = await self.w3.eth.get_balance(Account.from_key(private_key).address)
        return Decimal(self.w3.from_wei(balance_wei, "ether"))

    async def send_transaction(self, to_address: str, amount: Decimal) -> str:
        """
        Send BNB from master wallet to another.

        Args:
            to_address (str): The recipient wallet address.
            amount (Decimal): The amount of BNB to send.

        Returns:
            str: The transaction hash.
        """
        master_account = Account.from_key(settings.MASTER_PRIVATE_KEY)

        nonce = await self.w3.eth.get_transaction_count(master_account.address)
        gas_price = await self.w3.eth.gas_price

        transaction = {
            "to": to_address,
            "value": self.w3.to_wei(amount, "ether"),
            "gas": 21000,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": self.CHAIN_ID,
        }

        signed_txn = self.w3.eth.account.sign_transaction(transaction, master_account.key)
        tx_hash = await self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return self.w3.to_hex(tx_hash)
