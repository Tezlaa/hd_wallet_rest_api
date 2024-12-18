from sqlalchemy import func, select

from app.database.base.managers import BaseModelManager
from app.database.wallet.model import Wallet


class WalletManager(BaseModelManager):
    model = Wallet

    async def get_last_pk(self) -> int | None:
        stm = select(func.max(self.model.id))
        result = await self.session.execute(stm)
        return result.scalar()
