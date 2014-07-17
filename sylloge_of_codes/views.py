import random

from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.exceptions import NotFound
from pyramid.response import Response
from pyramid.url import route_url
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.i18n import get_locale_name, TranslationStringFactory
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from .models import (
    DBSession,
    Sylloge,
    Media,
    )

from wkhtmltopdf import wkhtmltopdf

import textile

import colander
from deform import Form, ValidationFailure, Button
from deform.widget import TextAreaWidget, HiddenWidget, TextInputWidget

from models import Curator

_ = TranslationStringFactory("sylloge_of_codes")

@notfound_view_config(renderer = "templates/notfound.pt")
def notfound_view(request):
    request.response.status = 404
    return dict(title = "404 Not Found", notfound = request.exception.args[0])

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {"title": "Sylloge of Codes Homepage"}

@view_config(route_name='submit', renderer='templates/submit.pt')
def submit(request):
    session = DBSession()

    # TODO
    # Not sure if this is the best way of doing things, but it's the only way I can think of to pass in the locale from the request, without jumping through a lot of hoops
    class Code(colander.Schema):
        code = colander.SchemaNode(colander.String(), title = _("Code"), widget = TextAreaWidget(rows = 6, css_class = "form-control"), missing_msg = _("Error: you must enter a code"),)
        comments = colander.SchemaNode(colander.String(), title = _("(Optional) Comments about this idea?"), missing = '', widget = TextAreaWidget(rows = 6, css_class = "form-control"))
        pseudonym = colander.SchemaNode(colander.String(), title = _("Pseudonym"), widget = TextInputWidget(css_class = "form-control"))
        _LOCALE_ = colander.SchemaNode(colander.String(), widget = HiddenWidget(), default = get_locale_name(request))
    
    form = Form(Code(), buttons=[Button("submit", _("Submit"), css_class = "btn btn-primary btn-lg")])

    if "submit" in request.POST:
        controls = request.POST.items()

        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            return {"title": "Sylloge of Codes Homepage", "form": e.render()}

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
        
        # TODO
        # setup sessions
        request.session.flash(_("Code was submitted successfully."))
        url = request.route_url("submitted")
        return HTTPFound(location=url)
    else:
        return {"title": "Sylloge of Codes Homepage", "form":form.render()}

@view_config(route_name="credits", renderer="templates/credits.pt")
def credits(request):
    return {"title": "Sylloge of Codes Credits"}

@view_config(route_name="about", renderer="templates/about.pt")
def about(request):
    return {"title": "Sylloge of Codes Credits"}

@view_config(route_name="print_test", renderer="templates/print_test.pt")
def print_test(request):
    session = DBSession()

    rand = random.randrange(0, session.query(Sylloge).filter(Sylloge.pdf_processed == 1).count())
    row = session.query(Sylloge)[rand]

    code = row.code
    code_date = row.code_date
    pseudonym = row.pseudonym

    return {"title": "Sylloge of Codes Credits", "code_item": "Submitted on %s by %s: %s" % (pseudonym, code_date, code)}

@view_config(route_name="submitted", renderer="templates/submitted.pt")
def print_page(request):
    session = DBSession()
    rand = random.randrange(0, session.query(Sylloge).filter(Sylloge.pdf_processed == 1).count())
    row = session.query(Sylloge)[rand]


    return {"title": "Sylloge of Codes Thanks", "pdf_url": row.pdf_path}

@view_config(route_name="sylloge", renderer="templates/sylloge.pt")
def sylloge(request):
    return {}

@view_config(route_name="render_pdf", renderer="templates/render_pdf.pt")
def render_pdf(request):
    session = DBSession()
    matchdict = request.matchdict
    
    try:
        code_result = session.query(Sylloge).filter(Sylloge.id == matchdict["code_id"]).one()
    except NoResultFound:
        raise HTTPNotFound("No code found.")

    code = code_result.code
    date = code_result.code_date
    pseudonym = code_result.pseudonym

    return {"title": "Sylloge of Codes Selection", "code": textile.textile(code), "date": date, "pseudonym": pseudonym}

@view_config(route_name="sylloge_code", renderer="templates/sylloge_code.pt")
def sylloge_code(request):
    return {}

# Authorized sections
@view_config(route_name = "login", renderer = "templates/login.pt")
@forbidden_view_config(renderer = "templates/login.pt")
def login(request):
    login_url = route_url("login", request)
    logged_in = authenticated_userid(request)

    if (logged_in):
        request.session.flash(_("You are already logged in."))
        return HTTPFound(location = route_url("home", request))

    referrer = request.url
    if referrer == login_url:
        referrer = "/" # never use the Login form itself as came_from

    came_from = request.params.get("came_from", referrer)
    login = ""
    password = ""
    
    if "submitted" in request.params:
        session = DBSession()
        login = request.params["login"]
        password = request.params["password"]

        if (Curator.checkPassword(login, password)):
            request.session["username"] = login
            headers = remember(request, Curator.getID(login))
            request.session.flash(_("You are now logged in."))
            return HTTPFound(location = came_from, headers = headers)

        request.session.flash(_("Failed login"))

    return dict(
            url = request.application_url + "/login",
            came_from = came_from,
            login = login,
            password = password,
            title = _("Sylloge of Codes Login"),
            )

@view_config(route_name = "logout")
def logout(request):
    headers = forget(request)
    request.session.flash(_("You have been logged out."))
    return HTTPFound(location = route_url("home", request), headers = headers)

@view_config(route_name = "curate", renderer = "templates/curate.pt", permission = "admin")
def curate(request):
    return {"title":_("Sylloge of Codes Curate")}

@view_config(route_name = "admin", renderer = "templates/admin.pt", permission = "admin")
def admin(request):
    return {"title":_("Sylloge of Codes Admin")}


#@view_config(renderer = "templates/notfound.pt", context = NotFound)

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

