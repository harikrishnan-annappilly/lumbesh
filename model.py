from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///data.db')
Base = declarative_base()


class CodeModel(Base):
    __tablename__ = 'codes'
    id = Column(Integer, primary_key=True)
    message_id = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.now)

    def __init__(self, message_id, code):
        self.message_id = message_id
        self.code = code

    def json(self):
        return {
            'id': self.id,
            'message_id': self.message_id,
            'code': self.code,
        }


Session = sessionmaker(bind=engine)
