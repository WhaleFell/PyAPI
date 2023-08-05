import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import dy, onedrive
from utils import logger, setLogLevel
from middleware import ProcessTimerMiddleware
# https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path
from config import makeConfig

ROOTPATH = Path(__file__).parent.absolute()
if os.environ.get('DEV'):
    logger.info("Current in Develop use config_dev.yaml")
    config = makeConfig(Path(ROOTPATH, "config_dev.yaml"))
else:
    logger.info("Current in Production use config.yaml")
    config = makeConfig(Path(ROOTPATH, "config.yaml"))

templates = Jinja2Templates(directory="static")


app = FastAPI(debug=True)
app.include_router(dy.router)
app.include_router(onedrive.router)

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
    logger.info(f"Run config:{config}")
    setLogLevel(config.LogLevel)
    uvicorn.run(
        "main:app",
        host=config.bind,
        port=config.port,
        reload=config.reload,
        workers=config.worker
    )
