from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.async_base import Base
from app.database.base.custom_types import unique_str, intpk


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[intpk] = mapped_column(comment="Wallet index")
    address: Mapped[unique_str] = mapped_column(index=True, comment="Wallet address")
    private_key: Mapped[unique_str] = mapped_column(comment="Wallet private key")
    public_key: Mapped[unique_str] = mapped_column(comment="Wallet public key")

    transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")
