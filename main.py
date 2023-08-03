import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import dy
from utils import logger
from middleware import ProcessTimerMiddleware
# https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from pathlib import Path
from models import Config
import yaml

ROOTPATH = Path(__file__).parent.absolute()
templates = Jinja2Templates(directory="static")


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
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
