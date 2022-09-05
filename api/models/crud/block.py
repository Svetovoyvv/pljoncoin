from sqlalchemy.orm import Session
from ..block import Block


class BlockCRUD:
    @classmethod
    def get(cls, db: Session, *, block_bc_id: int | None = None, block_id: int | None = None) -> Block | None:
        if block_bc_id is not None:
            m = db.query(Block).where(Block.bc_id == block_bc_id).first()
        elif block_id is not None:
            m = db.query(Block).where(Block.id == block_id).first()
        else:
            raise ValueError('Invalid arguments')
        return m
    @classmethod
    def get_transactions(cls, db: Session, block_id: int) -> list[str]:
        block = db.query(Block).where(Block.id == block_id).first()
        if block is None:
            return []
        return [i.tx_hash for i in block.transactions]
    @classmethod
    def add(cls, db: Session, block: Block) -> Block:
        db.add(block)
        db.commit()
        db.refresh(block)
        return block
