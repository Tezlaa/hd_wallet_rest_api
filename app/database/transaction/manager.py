from decimal import Decimal

from sqlalchemy import select

from app.database.base.managers import BaseModelManager
from app.database.transaction.model import Transaction


class TransactionManager(BaseModelManager):
    model = Transaction

    async def get_filtered_transactions(
        self,
        wallet_id: int,
        currency: str | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
        transaction_hash: str | None = None,
    ) -> list[Transaction]:
        stmt = select(self.model).where(self.model.wallet_id == wallet_id)

        if currency:
            stmt = stmt.filter(Transaction.currency == currency)
        if min_amount is not None:
            stmt = stmt.filter(Transaction.amount >= min_amount)
        if max_amount is not None:
            stmt = stmt.filter(Transaction.amount <= max_amount)
        if transaction_hash:
            stmt = stmt.filter(Transaction.transaction_hash == transaction_hash)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
