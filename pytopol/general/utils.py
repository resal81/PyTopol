
import logging
from urllib2 import urlopen
from pytopol import __version__ as local_version


def setup_logging(debug_level=logging.DEBUG):
    """ Setup initial logging.

    Args:
        debug_level: the level for debugging
    Returns:
        a logging.Logger instance

    """

    logger = logging.getLogger('mainapp')
    logger.setLevel(debug_level)

    frmt = logging.Formatter('%(name)-30s - %(levelname)-8s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(debug_level)
    ch.setFormatter(frmt)

    logger.addHandler(ch)

    return logger


def version_info():
    try:
        r = urlopen('https://raw.github.com/resal81/PyTopol/master/pytopol/__init__.py', timeout=1)
        txt = r.read()
        txtlist = txt.split()
        online_version = txtlist[-1]
        return {'online':online_version, 'local':local_version}, ''
    except Exception as e:
        msg = 'could not check online version: %s' % e
        return {'online':None, 'local':local_version}, msg