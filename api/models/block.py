import sqlalchemy as db
from sqlalchemy.orm import relationship
from . import Base
from pydantic import BaseModel, Field

class Block(Base):
    __tablename__ = 'blocks'
    id = db.Column(db.Integer, primary_key=True)
    bc_id = db.Column(db.Integer, nullable=False)
    transactions = relationship('Transaction', back_populates='block')
    logs = relationship('LogEntry', back_populates='block')
