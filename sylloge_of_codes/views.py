import random

from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.response import Response
from pyramid.url import route_url
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Sylloge,
    Media,
    )

from wkhtmltopdf import wkhtmltopdf

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {"title": "Sylloge of Codes Homepage", "project": "Sylloge of Codes"}

@view_config(route_name="code_submit", renderer="templates/code_submit.pt")
def code_submit(request):
    session = DBSession()
    if "form.submitted" in request.params:
        # TODO
        # Add in some sort of form validation, as in the Fluid Nexus website
        code = request.params["code"]
        comments = request.params["comments"]
        pseudonym = request.params["pseudonym"]
        try:
            mediaFilePath = request.params["mediaFilePath"]

            # TODO
            # Add in code for uploading media, if a path exists
        except KeyError:
            mediaFilePath = None

        code = Sylloge(code = code, comments = comments, pseudonym = pseudonym)
        session.add(code)

        return {"title": "Thanks!"}

    return HTTPFound(location = route_url("home", request))

@view_config(route_name="credits", renderer="templates/credits.pt")
def credits(request):
    return {"title": "Sylloge of Codes Credits"}

@view_config(route_name="about", renderer="templates/about.pt")
def about(request):
    return {"title": "Sylloge of Codes Credits"}

@view_config(route_name="print_test", renderer="templates/print_test.pt")
def print_test(request):
    session = DBSession()

    rand = random.randrange(0, session.query(Sylloge).count())
    row = session.query(Sylloge)[rand]

    code = row.code
    code_date = row.code_date
    pseudonym = row.pseudonym

    return {"title": "Sylloge of Codes Credits", "code_item": "Submitted on %s by %s: %s" % (pseudonym, code_date, code)}

@view_config(route_name="print", renderer="templates/print.pt")
def print_page(request):
    wkhtmltopdf(url="http://localhost:6543/print_test", output_file = "/Users/nknouf/Dropbox/projects/sylloge_of_codes/web/sylloge_of_codes/sylloge_of_codes/sylloge_of_codes/static/pdf/print_test.pdf")

    return {"title": "Sylloge of Codes Print", "pdf_url": "/static/pdf/print_test.pdf"}

@view_config(route_name="sylloge", renderer="templates/sylloge.pt")
def sylloge(request):
    return {}

@view_config(route_name="sylloge_code", renderer="templates/sylloge_code.pt")
def sylloge_code(request):
    return {}

@view_config(route_name="admin", renderer="templates/admin.pt")
def admin(request):
    return {}

@view_config(route_name="admin_curate", renderer="templates/admin_curate.pt")
def admin_curate(request):
    return {}


#def my_view(request):
#    try:
#        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#    except DBAPIError:
#        return Response(conn_err_msg, content_type='text/plain', status_int=500)
#    return {'one': one, 'project': 'sylloge_of_codes'}
#
#conn_err_msg = """\
#Pyramid is having a problem using your SQL database.  The problem
#might be caused by one of the following things:
#
#1.  You may need to run the "initialize_sylloge_of_codes_db" script
#    to initialize your database tables.  Check your virtual 
#    environment's "bin" directory for this script and try to run it.
#
#2.  Your database server may not be running.  Check that the
#    database server referred to by the "sqlalchemy.url" setting in
#    your "development.ini" file is running.
#
#After you fix the problem, please restart the Pyramid application to
#try it again.
#"""

