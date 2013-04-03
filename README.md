About
=====

This repo contains the source code for the Electronic Lending Tracking System
(ELTS).

Project Layout
==============

The branches, tags, and trunk folders are used in the usual way. If you don't
understand how branching under subversion works, go do some reading
[here](http://svnbook.red-bean.com/en/1.5/svn.branchmerge.html).

Django can collect static files, such as CSS files, into a central location for
you. You can then have a webserver serve those files, and the django app will
worry about just dynamic content. This is done with the `django-admin.py
collectstatic` command, and the resultant files are placed in the
`collectstatic` folder. The contents of the `collectstatic` folder should *not*
be version controlled.

This application requires a database backend to function. By default, ELTS is
configured to use sqlite3. When the `manage.py syncdb` command is run, a
database file will automatically be created in the `sqlite` folder if
necessary. The system administrator deploying this application can then choose
to use a different database backend as necessary. The contents of the `sqlite`
folder should *not* be version controlled.
