from typing import Annotated
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.clients.bsc_client import BSC_Client
from app.schemas.wallet import GeneratedWalletResponse
from app.schemas.transaction import TransactionSchema
from app.database.sessions import get_async_session
from app.database.wallet.manager import WalletManager
from app.database.wallet.model import Wallet
from app.database.transaction.manager import TransactionManager
from app.dependecies import get_wallet_object
from app.configs import settings


wallet_router = APIRouter(
    prefix="/wallet",
)


@wallet_router.post("/generate", response_model=GeneratedWalletResponse)
async def generate_wallet(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict[str, str]:
    """
    Generate new wallet. Auto increment index.
    """
    wallet_manager = WalletManager(session)
    last_index = await wallet_manager.get_last_pk()
    wallet_data = await BSC_Client().generate_wallet(last_index + 1 if last_index else 1)
    return await wallet_manager.create(**wallet_data.model_dump())


@wallet_router.get("/balance")
async def get_balance(
    wallet: Annotated[Wallet, Depends(get_wallet_object)],
) -> Decimal:
    """
    Get wallet balance.
    """
    return await BSC_Client().balance_check(wallet.private_key)


@wallet_router.post("/top-up", response_model=TransactionSchema)
async def topup_wallet(
    wallet: Annotated[Wallet, Depends(get_wallet_object)],
    amount: Decimal,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    """
    Top up wallet from master wallet.
    """
    master_balance = await BSC_Client().balance_check(settings.MASTER_PRIVATE_KEY)
    if master_balance < amount:
        raise HTTPException(status_code=400, detail=f"Not enough {abs(master_balance - amount)}")

    transaction_manager = TransactionManager(session)
    transaction = await transaction_manager.create(wallet_id=wallet.id, currency="BNB", amount=amount)

    transaction_hash = await BSC_Client().send_transaction(wallet.address, amount)

    return await transaction_manager.update(transaction, transaction_hash=transaction_hash)


@wallet_router.get("/transactions", response_model=list[TransactionSchema])
async def get_transactions(
    wallet: Annotated[Wallet, Depends(get_wallet_object)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    currency: str | None = Query(None, description="Currency name (BNB, ETH...)"),
    min_amount: Decimal | None = Query(None, description="Min amount of transaction"),
    max_amount: Decimal | None = Query(None, description="Max amount of transaction"),
    transaction_hash: str | None = Query(None, description="Transaction hash"),
) -> list[TransactionSchema]:
    transaction_manager = TransactionManager(session)
    return await transaction_manager.get_filtered_transactions(
        wallet_id=wallet.id,
        currency=currency,
        min_amount=min_amount,
        max_amount=max_amount,
        transaction_hash=transaction_hash,
    )
