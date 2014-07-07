import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid_chameleon',
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'Babel',
    'lingua',
    'pytz',
    ]

setup(name='sylloge_of_codes',
      version='0.0',
      description='sylloge_of_codes',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      message_extractors = {".":[
          ("**.py", "lingua_python", None),
          ("**.pt", "lingua_xml", None),
      ]},
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='sylloge_of_codes',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = sylloge_of_codes:main
      [console_scripts]
      initialize_sylloge_of_codes_db = sylloge_of_codes.scripts.initializedb:main
      """,
      )
