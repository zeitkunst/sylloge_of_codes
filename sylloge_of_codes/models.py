from datetime import datetime
import pytz

from pyramid.security import (
        Allow,
        Everyone,
        )

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, "view"),
            (Allow, "group:curators", "edit")]

    def __init__(self, request):
        pass

class Media(Base):
    """Model class for a Media object"""
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    code_id = Column(Integer)
    media_path = Column(Text(convert_unicode=True))

    def __init__(self, code_id = None, media_path = None):
        self.code_id = code_id
        self.media_path = media_path


class Sylloge(Base):
    """The SQLAlchemy declarative model class for a Codec object"""
    __tablename__ = "sylloge"
    id = Column(Integer, primary_key=True)
    code = Column(Text(convert_unicode=True))
    comments = Column(Text(convert_unicode=True))
    pseudonym = Column(Text(convert_unicode=True))
    code_date = Column(DateTime)
    enabled = Column(Boolean)
    media_id = Column(Integer, ForeignKey("media.id"))

    media = relationship(Media, backref=backref("sylloge", order_by=id))

    def __init__(self, code = None, comments = None, pseudonym = None, code_date = datetime.now(pytz.utc), mediaFilePath = None):
        self.code = code
        self.comments = comments
        self.pseudonym = pseudonym
        self.code_date = code_date
        self.mediaFilePath = mediaFilePath

        self.addMedia()

    def addMedia(self):
        pass


#Index('sylloge_index', Sylloge.code, unique=True, mysql_length=255)
