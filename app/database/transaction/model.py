from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.async_base import Base
from app.database.wallet.model import Wallet
from app.database.base.custom_types import intpk, unique_str


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[intpk] = mapped_column()
    currency: Mapped[str] = mapped_column(comment="Currency")
    amount: Mapped[Decimal] = mapped_column(Numeric, comment="Amount transaction")
    transaction_hash: Mapped[unique_str] = mapped_column(comment="Transaction hash", nullable=True, default=None)
    wallet_id: Mapped[Wallet] = mapped_column(ForeignKey("wallet.id"), comment="Wallet id that make the transaction")

    wallet = relationship("Wallet", back_populates="transactions")
