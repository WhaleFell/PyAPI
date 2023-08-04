# creat config object by `config.yaml`
import yaml
from utils import logger
from pathlib import Path
from models import Config


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
            logger.info(f"load {file} Success!")
            return Config(**conf)
    except Exception as e:
        logger.critical(f"load {file} error:{e}")
        logger.error(f"start by default config!")
        return Config()