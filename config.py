# creat config object by `config.yaml`
import yaml
from utils import logger
from pathlib import Path
from models import Config
import sys
import asyncio

# Only preform check if your code will run on non-windows environments.
if sys.platform == 'win32':
    # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def makeConfig(file: Path) -> Config:
    """load config in file and return Config Object

    Args:
        file (Path): file path

    Returns:
        Config: Config
    """
    try:
        with open(str(file)) as y:
            conf = yaml.safe_load(y)
            logger.success(f"load {file} Success!")
            return Config(**conf)
    except Exception as e:
        logger.critical(f"load {file} error:{e}")
        logger.error(f"start by default config!")
        return Config()
