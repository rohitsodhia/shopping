from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Item, Receipt


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item: Mapped["Item"] = relationship(
        back_populates="purchases", lazy="joined", innerjoin=True
    )
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))
    receipt: Mapped["Receipt"] = relationship(back_populates="purchases")
    price: Mapped[int] = mapped_column(Integer(), nullable=True)
    amount: Mapped[str | None] = mapped_column(String(), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text(), nullable=True)
