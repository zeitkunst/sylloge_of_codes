from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # pdf_processed is really a boolean, but sqlite doesn't have booleans, and if I use the sqlalchemy Boolean type, it causes oh-so-many-problems with the downgrade scripts (see https://code.google.com/p/sqlalchemy-migrate/issues/detail?id=143)
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    sylloge = Table('sylloge', meta, autoload = True)
    pdf_path = Column('pdf_path', Text)
    pdf_processed = Column('pdf_processed', Integer)
    pdf_path.create(sylloge)
    pdf_processed.create(sylloge)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    sylloge = Table('sylloge', meta, autoload = True)
    sylloge.c.pdf_processed.drop()
    sylloge.c.pdf_path.drop()
