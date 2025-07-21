from loguru import logger
import sys

__all__ = ["setup_logging","enable_debug"]

def setup_logging(debug: bool = False) -> None:
    '''Configure loguru logger level.

    Parameters
    ----------
    debug: bool
        Whether to enable debug level logs. if ``False``(default),
        logger will output messages with level INFO and above.
    '''

    level = "DEBUG" if debug else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=level)


def enable_debug() -> None:
    '''Convenience wrapper to enable debug level logging.'''
    setup_logging(True)
