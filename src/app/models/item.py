from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Purchase


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True)
    purchases: Mapped[list["Purchase"]] = relationship(back_populates="item")
    notes: Mapped[str] = mapped_column(Text(), nullable=True)
