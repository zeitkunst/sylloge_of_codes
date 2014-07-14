from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
            root_factory="sylloge_of_codes.models.RootFactory")
    config.include('pyramid_chameleon')
    config.add_translation_dirs("sylloge_of_codes:locale")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('code_submit', '/code_submit')
    config.add_route('about', '/about')
    config.add_route('credits', '/credits')
    config.add_route('sylloge', '/sylloge')
    config.add_route('sylloge_code', '/sylloge/{code_id}')
    config.add_route('admin', '/admin')
    config.add_route('admin_curate', '/admin_curate')
    config.add_route('print_test', '/print_test')
    config.add_route('print', '/print')
    config.scan()
    return config.make_wsgi_app()
