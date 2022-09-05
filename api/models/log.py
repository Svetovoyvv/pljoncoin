import sqlalchemy as db
from sqlalchemy.orm import relationship
from . import Base
from pydantic import BaseModel, Field
import datetime
class LogEntry(Base):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', back_populates='logs')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.id'))
    block = relationship('Block', back_populates='logs')
    ip = db.Column(db.String(64))
class TransactionPublic(BaseModel):
    tx_hash: str
    class Config:
        orm_mode = True
class BlockPublic(BaseModel):
    id: int = Field(..., title='Internal block ID', description='ID блока в базе')
    bc_id: int = Field(..., title='Blockchain block ID', description='ID блока в блокчейне')
    transactions: list[TransactionPublic] = Field([], title='Transactions', description='Список транзакций в блоке')
    class Config:
        orm_mode = True
class LogEntryPublic(BaseModel):
    created_at: datetime.datetime = Field(..., title='Date of log entry', description='Дата и время выполнения запроса')
    block_id: int = Field(..., title='Block ID', description='ID блока в сети блокчейна')
    block: BlockPublic = Field(..., title='Block', description='Блок в сети блокчейна')
    class Config:
        orm_mode = True
class LogEntryPrivate(LogEntryPublic):
    ip: str = Field(..., title='IP address', description='IP адрес пользователя, который выполнил поиск')
    class Config:
        orm_mode = True
class LogHistoryPublic(BaseModel):
    logs: list[LogEntryPublic] = Field(..., title='Logs', description='Список логов')
    count: int = Field(..., title='Count', description='Количество логов')
    class Config:
        orm_mode = True
class LogHistoryPrivate(BaseModel):
    logs: list[LogEntryPrivate] = Field(..., title='Logs', description='Список логов')
    count: int = Field(..., title='Count', description='Количество логов')
    class Config:
        orm_mode = True
