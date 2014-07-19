from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sylloge_of_codes.security import groupfinder

from sqlalchemy import event
from colanderalchemy import setup_schema
from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = session_factory_from_settings(settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy("sylloge_of_codes", callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
            root_factory="sylloge_of_codes.models.RootFactory")
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_session_factory(session_factory)
    config.include('pyramid_chameleon')
    config.include('pyramid_beaker')
    config.add_translation_dirs("sylloge_of_codes:locale")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('submit', '/submit')
    config.add_route('submitted', '/submitted')
    config.add_route('about', '/about')
    config.add_route('credits', '/credits')
    config.add_route('sylloge', '/sylloge')
    config.add_route('sylloge_code', '/sylloge/{code_id}')
    config.add_route('render_pdf', '/render_pdf/{code_id}')
    config.add_route('print_test', '/print_test')
    config.add_route('print', '/print')

    # Routes that need authentication
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('curate_nopagenum', '/curate')
    config.add_route('curate', '/curate/{page_num}')
    config.add_route('admin', '/admin')
    config.add_route('shutdown', '/admin/shutdown')
    config.scan()
    return config.make_wsgi_app()
