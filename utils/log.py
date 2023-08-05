from loguru import logger
import sys

def setLogLevel(level:str):
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> | {name}:{function} {level} | <level>{message}</level>",
        level=level,
        backtrace=True,
        diagnose=True
    )

# default logger
setLogLevel("DEBUG")
