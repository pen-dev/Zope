##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zExceptions import (
    HTTPException,
    InternalError,
)

ERROR_HTML = """\
<!DOCTYPE html>
<html>
<head>
<title>Site Error</title>
<meta charset="utf-8" />
</head>
<body bgcolor="#FFFFFF">
<h2>Site Error</h2>
<p>An error was encountered while publishing this resource.
</p>
<p><strong>Sorry, a site error occurred.</strong></p>

%s
<hr noshade="noshade"/>

<p>Troubleshooting Suggestions</p>

<ul>
<li>The URL may be incorrect.</li>
<li>The parameters passed to this resource may be incorrect.</li>
<li>A resource that this resource relies on may be
  encountering an error.</li>
</ul>

<p>If the error persists please contact the site maintainer.
Thank you for your patience.
</p>
</body></html>"""


class HTTPExceptionHandler(object):

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        environ['Zope2.httpexceptions'] = self
        try:
            return self.application(environ, start_response)
        except HTTPException as exc:
            return exc(environ, start_response)
        except Exception as exc:
            return self.catch_all_response(exc)(environ, start_response)

    def catch_all_response(self, exc):
        response = InternalError()
        response.setBody(ERROR_HTML % repr(exc))
        return response


def main(app, global_conf=None):
    return HTTPExceptionHandler(app)
