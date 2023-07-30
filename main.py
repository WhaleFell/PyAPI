import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import dy
from utils import logger
from middleware import ProcessTimerMiddleware
# https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from pathlib import Path
import yaml

ROOTPATH = Path(__file__).parent.absolute()


class Config(BaseModel):
    """
    uvicorn config
    """
    bind: str = "0.0.0.0"
    port: int = 8000
    LogLevel: str = "DEBUG"
    worker: int = 2  # 工作线程
    reload: bool = False  # 是否热重载


config = Config()

app = FastAPI(debug=True)
app.include_router(dy.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
process_time_middleware = ProcessTimerMiddleware()
app.add_middleware(BaseHTTPMiddleware, dispatch=process_time_middleware)


@app.get("/")
async def root():
    return "PyAPI Welcome"

if __name__ == "__main__":
    logger.info(f"ROOTPATH:{ROOTPATH}")

    try:
        with open(str(Path(ROOTPATH, "config.yaml"))) as y:
            conf = yaml.safe_load(y)
            config = config.model_validate(conf)
            logger.level(config.LogLevel)
    except Exception as e:
        logger.critical(f"load config.yaml error:{e}")
        logger.error(f"start by default config!")

    logger.info(f"Run config:{config}")
    uvicorn.run(
        "main:app",
        host=config.bind,
        port=config.port,
        reload=config.reload,
        workers=config.worker
    )
