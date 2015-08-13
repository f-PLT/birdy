import urlparse
import base64
from os.path import curdir, abspath, join

import logging
logger = logging.getLogger(__name__)

def fix_local_url(url):
    """
    If url is just a local path name then create a file:// URL. Otherwise return url just as it is.
    """
    u = urlparse.urlsplit(url)
    if not u.scheme:
        # build local file url
        path = u.path.strip()
        if path.startswith('/'):
            # absolute path
            url = urlparse.urljoin('file://', path)
        else:
            # relative path
            url = urlparse.urljoin('file://', abspath(path))
        logger.debug("fixed url = %s", url)
    return url

def encode(path, mimetypes):
    """
    Read file with given path and return content. If mimetype of file is binary then encode content with base64.

    :return: encoded content string or None
    """
    encoded = None
    with open(path, 'r') as fp:
        content = fp.read()
        # TODO: check all mimetypes ... use also python-magic to detect mime type
        if len(mimetypes) == 0 or mimetypes[0].lower() == 'application/xml' or mimetypes[0].lower().startswith('text/'):
            encoded = str(content)
        else:
            encoded = base64.b64encode(content)
    return encoded