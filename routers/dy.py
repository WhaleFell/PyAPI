from fastapi import Query
from typing_extensions import Annotated
from . import APIRouter
from utils.Douyin_video import DyVedio
from models import BaseAPI
from utils import logger
# https://fastapi.tiangolo.com/zh/advanced/custom-response/?h=or#orjsonresponse 压榨性能

router = APIRouter()
dy = DyVedio()


@router.get("/dy/", tags=["dy"])
async def dyVedio(
    url: Annotated[str, Query(
        title="抖音分享链接",
        description="复制目标链接自动提取文字中的链接")]
) -> BaseAPI:
    vid = await dy.getVedioID(url)
    logger.info("get the video id:%s" % vid)
    try:
        v_data = await dy.reqAPI(vid)
        r = BaseAPI(
            code=200,
            msg="解析成功！",
            content=v_data
        )
    except Exception as e:
        r = BaseAPI(
            code=400,
            msg=f"解析失败,请重试:{e}",
            content=None
        )

    return r
