from contextlib import contextmanager
import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session



Base = declarative_base()
engine = create_engine(settings.database_url)
Session = scoped_session(sessionmaker(bind=engine))

@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.expire_on_commit = True

def init_db():
    import app.models.log
    import app.models.user
    Base.metadata.create_all(bind=engine)