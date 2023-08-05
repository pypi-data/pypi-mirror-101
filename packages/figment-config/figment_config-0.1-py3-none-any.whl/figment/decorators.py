from .exception import FigmentException
import logging

LOG = logging.getLogger(__name__)

def cli_entry(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except FigmentException as ex:
            LOG.error(ex)
    return wrapper
