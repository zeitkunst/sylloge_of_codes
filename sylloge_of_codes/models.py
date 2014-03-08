from datetime import datetime
import pytz

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Sylloge(Base):
    """The SQLAlchemy declarative model class for a Codec object"""
    __tablename__ = "sylloge"
    id = Column(Integer, primary_key=True)
    code = Column(Text(convert_unicode=True))
    comment = Column(Text(convert_unicode=True))
    pseudonym = Column(Text(convert_unicode=True))
    code_date = Column(DateTime)
    enabled = Column(Boolean)
    media_id = Column(Integer)

    def __init__(self, code = None, pseudonym = None, code_date = datetime.now(pytz.utc)):
        self.code = code
        self.pseudonym = pseudonym
        self.code_date = code_date

class Media(Base):
    """Model class for a Media object"""
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    code_id = Column(Integer)
    media_path = Column(Text(convert_unicode=True))

    def __init__(self, code_id = None, media_path = None):
        self.code_id = code_id
        self.media_path = media_path

#Index('sylloge_index', Sylloge.code, unique=True, mysql_length=255)
