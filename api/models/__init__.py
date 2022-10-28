import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_url = os.environ.get('SQL_CONNECTION_URL') or 'sqlite:///data.db'
connect_args = {}
if 'sqlite' in db_url:
    connect_args = {'check_same_thread': False}

while True:
    try:
        engine = create_engine(
            db_url,
            echo=os.environ.get('SQL_ECHO') == 'true',
            connect_args=connect_args
        )
        engine.connect()
        break
    except Exception as e:
        print('Ожидание подключения', e)
        time.sleep(3)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

print('Started on', engine)