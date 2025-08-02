from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    db_url = Column(String)
    admin_email = Column(String)
    admin_password = Column(String)
