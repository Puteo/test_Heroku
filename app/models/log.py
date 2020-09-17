from sqlalchemy import Column
from sqlalchemy import desc
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
from app.models.base import session_scope
from app.models.base import Session

class Logs(object):
    def __init__(self):
        self.logs = []
        self.log = Log()
    
    def set_all_logs(self, limit=10):
        self.logs = self.log.get_all_logs(limit)
        return self.logs

    def set_all_show_logs(self):
        self.logs = self.log.get_all_Show_logs()
        return self.logs

    def updata_all_show_logs(self):
        self.logs = self.log.get_all_Show_logs()
        if self.logs is None:
            pass
        else:
            for log in self.logs:
                log.show = -1
                log.save()

    def Delete_all_logs(self):
        self.logs = self.log.get_all_logs()
        for log in self.logs:
            log.delete()
            log.save()


class Log(Base):
    __tablename__ = "LogData"
    time = Column(DateTime, primary_key=True, nullable=False)
    name = Column(Text)
    message = Column(Text)
    show = Column(Integer)

    @classmethod
    def create(cls, time, name, message):
        log = cls(time=time,name=name,message=message,show=0)
        try:
            with session_scope() as session:
                session.add(log)
            return log
        except IntegrityError:
            return False

    @classmethod
    def DeleteAllRecord(cls):
        with session_scope() as session:
            logs = session.query(cls).all()
            for log in logs:
                session.delete(log)

    @classmethod
    def get(cls, time):
        with session_scope() as session:
            log = session.query(cls).filter(
                cls.time == time).first()
        if log is None:
            return None
        return log

    def save(self):
        with session_scope() as session:
            session.add(self)

    @classmethod
    def get_all_Show_logs(cls):
        with session_scope() as session:
            logs = session.query(cls).filter(
                cls.show == 0).order_by(
                desc(cls.time)).all()

        if len(logs) == 0:
            return None

        return logs

    @classmethod
    def get_all_logs(cls, limit=10):
        with session_scope() as session:
            logs = session.query(cls).order_by(
                desc(cls.time)).limit(limit).all()

        if len(logs) == 0:
            return None

        return logs
    
    @property
    def value(self):
        return {
            'time': self.time,
            'name': self.name,
            'message': self.message,
            'show': self.show,
        }