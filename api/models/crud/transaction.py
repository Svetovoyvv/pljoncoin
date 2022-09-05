from sqlalchemy.orm import Session
from . import BlockCRUD
from models.transaction import Transaction
class TransactionCRUD:
    @classmethod
    def add(cls, db: Session, block_id: int, *args: list[str] | tuple[list[str]]):
        if len(args) == 1 and isinstance(args[0], list | tuple):
            args = args[0]
        if BlockCRUD.get(db, block_id=block_id) is None:
            raise ValueError('Invalid block id')
        for i in args:
            db.add(Transaction(block_id=block_id, tx_hash=i))
        db.commit()

