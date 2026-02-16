from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship("Company", back_populates="employees")

    def __repr__(self):
        company_name = self.company.name if self.company else "UNEMPLOYED"

        return f"User(id={self.id!r}, email={self.email!r}, company={company_name!r})"
