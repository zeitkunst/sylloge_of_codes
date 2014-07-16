import os, sys

from pyramid.paster import get_appsettings
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import engine_from_config

from wkhtmltopdf import wkhtmltopdf

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker

from sylloge_of_codes.models import Sylloge

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv = sys.argv):
    if len(argv) != 2:
        usage(argv)

    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    
    # TODO
    # Getting this argument could be brittle...
    settings = get_appsettings(sys.argv[1])
    engine = engine_from_config(settings, "sqlalchemy.")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        results = session.query(Sylloge).filter(Sylloge.pdf_processed == 0)
    except NoResultFound:
        sys.exit(0)
    
    for result in results:
        id = result.id
        # TODO
        # This is brittle, but I don't know how to get the "server:main" section from the ini file
        path = "/static/pdf/rendered_%03d.pdf" % id
        wkhtmltopdf(url='http://localhost:6543/render_pdf/%d' % id, output_file = 'sylloge_of_codes%s' % path, page_size = "Letter", print_media_type = True)
        result.pdf_processed = 1
        result.pdf_path = path
        session.add(result)
        session.commit()

