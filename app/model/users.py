from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.session import Base




class Users(Base):
    __tablename__ = 'tbl_users'


    id = Column(Integer, primary_key=True)
    userId = Column(String, unique= True)
    username = Column(String, unique = True)
    email = Column(String, unique = True)
    first_name =Column(String, nullable=True)
    last_name =Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    password = Column(String, nullable=False)
    image_url_key = relationship("Images", back_populates="users_key")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    is_verified = Column(Boolean, nullable= False, default= False)
    



class Images(Base):
    __tablename__ = 'tbl_images'
    id = Column(Integer, primary_key=True)
    image_name = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    # Foreign key column in Images that references Users
    user_id = Column(Integer, ForeignKey('tbl_users.id'), nullable=False)
    users_key = relationship("Users", back_populates="image_url_key")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    