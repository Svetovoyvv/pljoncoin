import sqlalchemy as db
from sqlalchemy.orm import relationship
from . import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    tx_hash = db.Column(db.String(128))
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.id'))
    block = relationship('Block', back_populates='transactions')

