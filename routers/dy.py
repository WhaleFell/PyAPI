from fastapi import Query
from typing_extensions import Annotated
from fastapi import APIRouter
from utils.Douyin_video import DyVedio
from models import BaseAPI
from utils import logger
from httpx import HTTPError
from fastapi.responses import ORJSONResponse
# https://fastapi.tiangolo.com/zh/advanced/custom-response/?h=or#orjsonresponse 压榨性能

router = APIRouter()
dy = DyVedio()


@router.get("/dy/", tags=["dy"])
async def dyVedio(
    url: Annotated[str, Query(
        title="抖音分享链接",
        description="复制目标链接自动提取文字中的链接")]
) -> BaseAPI:
    """
    输入一段抖音app分享的文本链接,自动提取文本中的链接地址,进行抖音解析.
    """
    logger.debug("req url:%s" % url)
    try:
        vid = await dy.getVedioID(url)

        logger.info("get the video id:%s" % vid)
        v_data = await dy.reqAPI(vid)
        r = BaseAPI(
            code=200,
            msg="解析成功！",
            content=v_data
        )
    except HTTPError:
        r = BaseAPI(
            code=400,
            msg=f"HTTP RESP Error,Try Again.",
            content=None
        )
    except Exception as e:
        logger.exception("why dy api error:%s" % e)
        r = BaseAPI(
            code=400,
            msg=f"Unknown error:{e}",
            content=None
        )

    return r
