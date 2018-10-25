import logging
import logging.config

def log_config():
    logging.basicConfig(format='%(message)s', filename='logs/execution.log',level=logging.DEBUG)
    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)
    return LOG
