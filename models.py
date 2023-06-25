from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    items = relationship('Item', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}"


class Item(Base):
    ITEM_TYPES = (
        ('RAW_MATERIAL', 'raw_materials'),
        ('FINISHED_GOODS', 'finished_goods'),
        ('COMPONENTS', 'components')
    )

    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    item_name = Column(String(20), nullable=False)
    item_type = Column(ChoiceType(choices=ITEM_TYPES), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items')

    def __repr__(self):
        return f"<Items {self.id}>"
