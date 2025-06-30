import aiohttp
from loguru import logger

class Client:

    def __init__(self) -> None:
        pass

    def run(self, token: str):
        logger.debug("Your token is {}", token)
