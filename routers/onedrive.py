from fastapi import Query
from typing_extensions import Annotated
from fastapi import APIRouter
from utils.Douyin_video import DyVedio
from models import BaseAPI
from utils import logger
from httpx import HTTPError
from fastapi.responses import ORJSONResponse, PlainTextResponse


router = APIRouter()


@router.get("/onedrive/", tags=["dy"])
async def onedrive():
    return PlainTextResponse(content="Hello Onedrive!")
