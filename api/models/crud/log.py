from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.log import LogEntry, LogHistoryPublic, LogHistoryPrivate
class LogEntryCRUD:
    @classmethod
    def add(cls, db: Session, user_id: int, block_id: int, ip: str):
        db.add(LogEntry(
            user_id=user_id,
            block_id=block_id,
            ip=ip
        ))
        db.commit()
    @classmethod
    def get_history(cls,
                    db: Session,
                    user_id: int,
                    offset: int = 0,
                    limit: int = 10,
                    public: bool = True) -> LogHistoryPublic | LogHistoryPrivate:
        if public:
            model = LogHistoryPublic
        else:
            model = LogHistoryPrivate
        logs = db.query(LogEntry)\
            .where(LogEntry.user_id == user_id)\
            .order_by(desc(LogEntry.created_at))\
            .offset(offset).limit(limit).all()
        print(list(map(lambda a: a.block, logs)))
        count = db.query(LogEntry).where(LogEntry.user_id == user_id).count()
        return model(logs=logs, count=count)

