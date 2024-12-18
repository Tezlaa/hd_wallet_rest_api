from typing import Annotated, NoReturn

from fastapi import Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.wallet.model import Wallet
from app.database.wallet.manager import WalletManager
from app.database.sessions import get_async_session


async def get_wallet_object(
    wallet: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Wallet | NoReturn:
    """
    Take wallet address and return wallet object. If wallet not found raise HTTPException 404.
    """
    wallet_manager = WalletManager(session)
    wallet = await wallet_manager.get_one_or_none(address=wallet)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
