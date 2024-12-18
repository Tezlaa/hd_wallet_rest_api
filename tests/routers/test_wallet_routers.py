from decimal import Decimal

import pytest

from unittest.mock import AsyncMock

from app.common.clients.bsc_client import BSC_Client
from app.database.wallet.manager import WalletManager
from app.schemas.wallet import GeneratedWalletFullData


class TestWalletRouter:
    @pytest.mark.asyncio
    async def test_generate_wallet(self, monkeypatch, client, async_db_session):
        client_response = GeneratedWalletFullData(**{
            "address": "mock_address",
            "private_key": "mock_private_key",
            "public_key": "mock_public_key",
        })
        mock_generate_wallet = AsyncMock(return_value=client_response)
        monkeypatch.setattr(BSC_Client, "generate_wallet", mock_generate_wallet)

        response = await client.post("api/v1/wallet/generate")

        assert response.status_code == 200
        assert response.json() == {"address": "mock_address"}
        mock_generate_wallet.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_balance(self, monkeypatch, client, async_db_session):
        client_response = Decimal("0.0011")
        mock_balance_check = AsyncMock(return_value=client_response)
        monkeypatch.setattr(BSC_Client, "balance_check", mock_balance_check)

        wallet = await WalletManager(async_db_session).create(
            address="mock_address", private_key="mock_private_key", public_key="mock_public_key"
        )

        # wallet not found
        response = await client.get("api/v1/wallet/balance?wallet=1111")

        assert response.status_code == 404
        assert response.json() == {"detail": "Wallet not found"}
        mock_balance_check.assert_not_called()

        # wallet found
        response = await client.get(f"api/v1/wallet/balance?wallet={wallet.address}")

        assert response.status_code == 200
        assert response.json() == "0.0011"
        mock_balance_check.assert_called_once_with(wallet.private_key)

    @pytest.mark.asyncio
    async def test_topup_wallet(self, monkeypatch, client, async_db_session):
        client_response = "mock_transaction_hash"
        mock_send_transaction = AsyncMock(return_value=client_response)
        monkeypatch.setattr(BSC_Client, "send_transaction", mock_send_transaction)

        client_balance = Decimal("0.0011")
        mock_balance_check = AsyncMock(return_value=client_balance)
        monkeypatch.setattr(BSC_Client, "balance_check", mock_balance_check)

        wallet = await WalletManager(async_db_session).create(
            address="mock_address", private_key="mock_private_key", public_key="mock_public_key"
        )

        # not enough balance
        response = await client.post(f"api/v1/wallet/top-up?wallet={wallet.address}&amount=0.1")

        assert response.status_code == 400, response.json()
        assert response.json() == {"detail": "Not enough 0.0989"}
        mock_send_transaction.assert_not_called()

        # enough balance
        response = await client.post(f"api/v1/wallet/top-up?wallet={wallet.address}&amount=0.0001")

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "currency": "BNB",
            "amount": "0.0001",
            "wallet": {"address": "mock_address"},
            "transaction_hash": "mock_transaction_hash",
        }
        mock_send_transaction.assert_called_once_with(wallet.address, Decimal("0.0001"))

        mock_send_transaction.reset_mock()

        # wallet not found
        response = await client.post("api/v1/wallet/top-up?wallet=1111&amount=0.001")

        assert response.status_code == 404, response.json()
        assert response.json() == {"detail": "Wallet not found"}
        mock_send_transaction.assert_not_called()
