#vim: set fileencoding=utf-8
import os, re, sys, tempfile

from pyramid.paster import get_appsettings
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import engine_from_config

from wkhtmltopdf import wkhtmltopdf

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker

from sylloge_of_codes.models import Sylloge

xelatexDocument = r"""\documentclass[17pt,extrafontsizes,oneside]{memoir}

\setlrmarginsandblock{1.5in}{*}{*}
\setulmarginsandblock{1.25in}{*}{*}
\checkandfixthelayout
\setlength{\parindent}{0pt}
\nonzeroparskip

\usepackage{fontspec}
\usepackage{csquotes}
\usepackage{hyperref}
\usepackage{textcomp}

\setromanfont [BoldFont={Adobe Jenson Pro Bold}, ItalicFont={Adobe Jenson Pro Italic}]{Adobe Jenson Pro}
\setsansfont [BoldFont={Source Sans Pro Bold}, ItalicFont={Source Sans Pro Italic}]{Source Sans Pro}

\begin{document}
\pagestyle{empty}
\centerline{\textbf{\Huge\sffamily sylloge of codes}}

Contributed by \textit{%s} on %s.

%s

For more information about this project, please visit \url{http://sylloge-of-codes.net}.

\hrulefill

\textcopyright 2014, Nicholas Knouf and the respective contributors. All content is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (\url{http://creativecommons.org/licenses/by-nc/4.0/}).
\end{document}"""

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
       
        # Escape usual latex characters
        processedCode = ""
        processedCode = re.sub(r'\\', '\\\\textbackslash ', result.code)
        processedCode = re.sub(r'\^', '\\\\textasciicircum ', processedCode)
        processedCode = re.sub(r'~', '\\\\textasciitilde ', processedCode)
        processedCode = re.sub(r'([#\$%&_\{\}])', lambda m: "\%s" % m.group(1), processedCode)
        document = xelatexDocument % (result.pseudonym, str(result.code_date), processedCode)

        tempDir = tempfile.mkdtemp()
        xelatexFile = os.path.join(tempDir, "sylloge.tex")
        xelatexFilePDF = os.path.join(tempDir, "sylloge.pdf")
        
        # TODO
        # Brittle, as the path is hard-coded in...need to figure out a better way of doing this
        staticPath = "/static/pdf/sylloge_of_codes_%05d.pdf" % id
        #outputPath = os.path.join("/Users/nknouf/Dropbox/projects/sylloge_of_codes/web/sylloge_of_codes/sylloge_of_codes", staticPath)
        outputPath = "/Users/nknouf/Dropbox/projects/sylloge_of_codes/web/sylloge_of_codes/sylloge_of_codes/sylloge_of_codes" + staticPath
       

        try:
            with open(xelatexFile, "w") as f:
                f.write(document.encode("utf-8"))
        except (IOError, OSError, Failure) as e:
            print "Error: ", e
            continue
        
        print "Working on %s" % xelatexFile
        os.system("cd %s; latexmk -xelatex %s" % (tempDir, xelatexFile))
        os.system("mv %s %s" % (xelatexFilePDF, outputPath))

        # TODO
        # This is brittle, but I don't know how to get the "server:main" section from the ini file
        #path = "/static/pdf/rendered_%03d.pdf" % id
        #wkhtmltopdf(url='http://localhost:6543/render_pdf/%d' % id, output_file = 'sylloge_of_codes%s' % path, page_size = "Letter", print_media_type = True)
        result.pdf_processed = 1
        result.pdf_path = staticPath 
        session.add(result)
        session.commit()

