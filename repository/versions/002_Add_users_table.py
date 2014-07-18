from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from migrate import *

meta = MetaData()
Base = declarative_base()

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

class GroupInfo(Base):
    __label__ = "GroupInfo"
    __plural__ = "GroupInfos"
    __tablename__ = "group_info"

    id = Column(Integer, primary_key = True)
    group_name = Column(Unicode, nullable = False)
    description = Column(Unicode, nullable = False)

class Group(Base):
    __label__ = "Group"
    __plural__ = "Groups"
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key = True)
    curator_id = Column(Integer, ForeignKey('curator.id'), nullable = False)
    group_info_id = Column(Integer, ForeignKey('group_info.id'), nullable = False)

    curator = relationship(Curator, backref=backref('groups', order_by=id))
    group_info = relationship(GroupInfo, backref=backref('groups', order_by=id))
    
curator = Curator()

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    Curator.__table__.create(migrate_engine)
    Group.__table__.create(migrate_engine)
    GroupInfo.__table__.create(migrate_engine)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    Curator.__table__.drop(migrate_engine)
    Group.__table__.drop(migrate_engine)
    GroupInfo.__table__.drop(migrate_engine)
