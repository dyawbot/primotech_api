from sqlalchemy import Column, Integer, String
from config import Base




class Users(Base):
    __tablename__ = 'tbl_users'


    id = Column(Integer, primary_key=True)
    userId = Column(String)
    username = Column(String)