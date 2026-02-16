from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Company(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    website_url = Column(String)
    tax_id = Column(String)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", foreign_keys=[owner_id])
    employees = relationship("User", back_populates="company", foreign_keys="[User.company_id]")

    def __repr__(self):
        return f"Company(id={self.id!r}, name={self.name!r}, email={self.email!r})"
