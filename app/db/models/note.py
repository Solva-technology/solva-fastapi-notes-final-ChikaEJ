from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import MAX_LENGTH_CONTENT, MAX_LENGTH_TITLE
from app.core.db import Base


class Note(Base):
    title: Mapped[str] = mapped_column(String(MAX_LENGTH_TITLE),
                                       nullable=False)
    content: Mapped[str] = mapped_column(String(MAX_LENGTH_CONTENT),
                                         nullable=True)
    is_public: Mapped[bool] = mapped_column(default=True)
    is_completed: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship("User",
                                        back_populates="notes")
