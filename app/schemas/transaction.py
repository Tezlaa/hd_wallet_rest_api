from decimal import Decimal

from pydantic import BaseModel

from app.schemas.wallet import GeneratedWalletResponse


class TransactionSchema(BaseModel):
    id: int
    currency: str
    amount: Decimal
    wallet: GeneratedWalletResponse
    transaction_hash: str | None
