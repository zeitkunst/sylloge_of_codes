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
    Unicode,
    DateTime,
    Float,
    ForeignKey,
    event,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    mapper,
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import ZopeTransactionExtension

import bcrypt

from colanderalchemy import setup_schema

from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory("sylloge_of_codes")

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
event.listen(mapper, "mapper_configured", setup_schema)

    
class RootFactory(object):
    __acl__ = [ (Allow, Everyone, "view"),
            (Allow, "group:admin", "admin")]

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
    # REMEMBER! sqlite doesn't have boolean type, using it here will only cause problems with migration scripts later...
    __tablename__ = "sylloge"
    id = Column(Integer, primary_key=True)
    code = Column(Text(convert_unicode=True))
    comments = Column(Text(convert_unicode=True))
    pseudonym = Column(Text(convert_unicode=True))
    code_date = Column(DateTime)
    enabled = Column(Integer, default = 0) # really, boolean
    pdf_processed = Column(Integer, default = 0) # really, boolean
    pdf_path = Column(Text)
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

class Curator(Base):
    __label__ = "Curator"
    __plural__ = "Curators"
    __tablename__ = "curator"

    id = Column(Integer, primary_key = True)
    username = Column(Unicode, nullable = False)
    password = Column(Unicode, nullable = False)
    given_name = Column(Unicode)
    surname = Column(Unicode)
    created = Column(Float)
    email = Column(Unicode, default = u"")

    def __repr__(self):
        return "<Curator '%s'>" % self.username

    @classmethod
    def getByUsername(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def getByID(cls, user_id):
        return DBSession.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def checkPassword(cls, username, password):
        user = cls.getByUsername(username)
        if not user:
            return False

        hashed_password = DBSession.query(Curator.password).filter(Curator.username == username).one()[0]

        if bcrypt.hashpw(password.encode("utf-8"), hashed_password.encode("utf-8")) == hashed_password:
            return True
        else:
            return False

    @classmethod
    def getID(cls, username):
        return DBSession.query(cls.id).filter(cls.username == username).one()[0]
#Index('sylloge_index', Sylloge.code, unique=True, mysql_length=255)

class GroupInfo(Base):
    __label__ = "GroupInfo"
    __plural__ = "GroupInfos"
    __tablename__ = "group_info"

    id = Column(Integer, primary_key = True)
    group_name = Column(Unicode, nullable = False)
    description = Column(Unicode, nullable = False)

    def __repr__(self):
        return "<GroupInfo '%s'>" % self.group_name

    def __init__(self, group_name = "", description = ""):
        self.group_name = group_name
        self.description = description

class Group(Base):
    __label__ = "Group"
    __plural__ = "Groups"
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key = True)
    curator_id = Column(Integer, ForeignKey('curator.id'), nullable = False)
    group_info_id = Column(Integer, ForeignKey('group_info.id'), nullable = False)

    curator = relationship(Curator, backref=backref('groups', order_by=id))
    group_info = relationship(GroupInfo, backref=backref('groups', order_by=id))
    
    def __repr__(self):
        return "<Group '%d'>" % self.id


