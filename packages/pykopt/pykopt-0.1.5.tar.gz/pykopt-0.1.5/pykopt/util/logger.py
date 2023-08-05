import time
import logging


def current_time():
    return round(time.time() * 1000)


logger = logging.getLogger("Pykopt")

