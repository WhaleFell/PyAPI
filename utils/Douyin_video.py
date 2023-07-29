# download and get info to douyin vedio.
# support vedio and photos
"""
图文:
2.05 NJv:/ 复制打开抖音，看看【芽芽丸的图文作品】# 双相 药苦 命也苦  https://v.douyin.com/icjj7Ss/
视频:
5.33 KJV:/ 复制打开抖音，看看【民谣收录机(音乐分享)的作品】成年人的生活没有容易一说，小姐姐的眼神都是心疼# ... https://v.douyin.com/icjjVJV/

接口:
https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=
"""

import httpx
from . import logger
from pydantic import BaseModel
from pydantic import HttpUrl
from pathlib import Path
import urllib
import execjs
import asyncio
import re
from typing import Union, Any, List
# https://github.com/ijl/orjson
import orjson
import sys
import jsonpath

# Only preform check if your code will run on non-windows environments.
if sys.platform == 'win32':
    # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

BUGUSJSPATH = str(
    Path(
        Path(__file__).parent,
        "X-Bugus.js"
    )
)


class Author(BaseModel):
    nickname: str  # JSON.aweme_detail.author.nickname
    signature: str  # JSON.aweme_detail.author.signature
    head: HttpUrl  # JSON.aweme_detail.author.avatar_thumb.url_list[0]


class VedioDetail(BaseModel):
    id: str
    desc: str  # JSON.aweme_detail.desc
    author: Author
    # JSON.aweme_detail.video.play_addr_h264.url_list[0]
    video: Union[List[HttpUrl], HttpUrl, bool]
    mp3: HttpUrl  # JSON.aweme_detail.music.play_url.uri
    # JSON.aweme_detail.video.cover_original_scale.url_list[0]
    video_thum: Union[HttpUrl, bool]


class DyVedio(object):
    """抖音单个视频解析
    参考:https://github.com/B1gM8c/X-Bogus
    """

    def __init__(self) -> None:
        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Referer': 'https://www.douyin.com/',
            'Cookie': 'msToken=uTa38b9QFHB6JtEDzH9S4np17qxpG6OrROHQ8at2cBpoKfUb0UWmTkjCSpf72EcUrJgWTIoN6UgAv5BTXtCbOAhJcIRKyZIT7TMYapeOSpf;odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; ttwid=1%7CWBuxH_bhbuTENNtACXoesI5QHV2Dt9-vkMGVHSRRbgY%7C1677118712%7C1d87ba1ea2cdf05d80204aea2e1036451dae638e7765b8a4d59d87fa05dd39ff; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVKUDZzbjNLRlFBNUROSEcyK2F4bXAwNG5cclxud1hBSTZDU1IyZW1sVUE5QTZ4aGQzbVlPUlI4NVRLZ2tXd1FJSmp3Nyszdnc0Z2NNRG5iOTRoS3MvSjFJc3FBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnVmJkWTI0c0RYS0c0S2h3WlBmOHpxVDRBU0ROamNUb2FFRi9MQnd2QS8xSUNcclxuSURiVmZCUk1PQVB5cWJkcytld1QwSDZqdDg1czZZTVNVZEo5Z2dmOWlmeTBcclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9'
        }
        self.api = "https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=%s&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333&X-Bogus=DFSzswSLfwUANnEftawINt9WcBj3"

        self.bugusJS = open(BUGUSJSPATH).read()

    # 检索字符串中的链接

    @staticmethod
    def get_url(text: str) -> HttpUrl:
        try:
            # 从输入文字中提取索引链接存入列表/Extract index links from input text and store in list
            url = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # 判断是否有链接/Check if there is a link
            if len(url) > 0:
                return url[0]
        except Exception as e:
            logger.warning("Error in get_url input:%s" % text)
            return None

    # 生成抖音X-Bogus签名/Generate Douyin X-Bogus signature
    # 下面的代码不能保证稳定性，随时可能失效/ The code below cannot guarantee stability and may fail at any time
    def generate_x_bogus_url(self, url: str) -> str:
        """
        生成抖音X-Bogus签名
        :param url: 视频链接
        :return: 包含X-Bogus签名的URL
        """
        # 调用JavaScript函数
        query = urllib.parse.urlparse(url).query
        xbogus = execjs.compile(self.bugusJS).call(
            'sign', query, self.headers['User-Agent'])
        logger.debug('生成的X-Bogus签名为: {}'.format(xbogus))
        new_url = url + "&X-Bogus=" + xbogus
        return new_url

    async def getVedioID(self, rawUrl: Union[HttpUrl, str]) -> Union[str, None]:

        async with httpx.AsyncClient(headers=self.headers) as c:
            video_url = await c.get(self.get_url(rawUrl), follow_redirects=True)
            video_url = str(video_url.url)

        logger.debug(f"dump link:{video_url}")
        
        # 链接类型:
        # 视频页 https://www.douyin.com/video/7086770907674348841
        if '/video/' in video_url:
            key = re.findall('/video/(\d+)?', video_url)[0]
            logger.info("获取到的抖音视频ID为: {}".format(key))
            return key
        # 发现页 https://www.douyin.com/discover?modal_id=7086770907674348841
        elif 'discover?' in video_url:
            key = re.findall('modal_id=(\d+)', video_url)[0]
            logger.info("获取到的抖音视频ID为: {}".format(key))
            return key
        # 直播页
        elif 'live.douyin' in video_url:
            # https://live.douyin.com/1000000000000000000
            video_url = video_url.split(
                '?')[0] if '?' in video_url else video_url
            key = video_url.replace('https://live.douyin.com/', '')
            logger.info("获取到的抖音直播ID为: {}".format(key))
            return key
        # note
        elif 'note' in video_url:
            # https://www.douyin.com/note/7086770907674348841
            key = re.findall('/note/(\d+)?', video_url)[0]
            logger.info("获取到的抖音笔记ID为: {}".format(key))
            return key
        else:
            logger.error("无法识别链接类型")
            raise Exception("无法识别链接类型")

    async def reqAPI(self, vid: str) -> VedioDetail:
        api_url = self.generate_x_bogus_url(self.api % vid)
        async with httpx.AsyncClient(headers=self.headers) as client:
            logger.debug("gan api_url:%s" % api_url)
            r = await client.get(url=api_url)

            try:
                jsonData = orjson.loads(b"%s" % (r.content))
            except Exception:
                logger.error(
                    "Api repons not json data!len:%s" % (len(r.content)))
                return None

            # logger.debug(
            #     "api respon:\n%s" % (jsonData)
            # )

            # with open("api.json", "w", encoding="utf8") as f:
            #     import json
            #     f.write(str(json.dumps(jsonData, ensure_ascii=False)))

            au = jsonpath.jsonpath(jsonData, '$.aweme_detail.author')[0]
            na = jsonpath.jsonpath(au, '$.nickname')[0]
            au_url = jsonpath.jsonpath(au, '$.avatar_thumb.url_list[0]')[0]
            sign = jsonpath.jsonpath(au, "$.signature")[0]
            aud = Author(
                nickname=na,
                head=au_url,
                signature=sign
            )
            logger.debug(f"作者信息:{aud}")

            desc = jsonpath.jsonpath(jsonData, '$.aweme_detail.desc')[0]
            mp3 = jsonpath.jsonpath(
                jsonData, "$.aweme_detail.music.play_url.uri")[0]
            v_p = jsonpath.jsonpath(
                jsonData, "$.aweme_detail.video.cover_original_scale.url_list[0]")

            try:
                v_p = jsonpath.jsonpath(
                    jsonData, "$.aweme_detail.video.cover_original_scale.url_list[0]")[0]
                video_url = jsonpath.jsonpath(
                    jsonData, '$.aweme_detail.video.play_addr_h264.url_list[0]')[0]
            except Exception as e:
                logger.debug("按视频解析出错,接下来按图文解析")
                v_p = jsonpath.jsonpath(
                    jsonData, "$.aweme_detail.video.origin_cover.url_list[0]")[0]
                video_url = []
                for img in jsonData["aweme_detail"]["images"]:
                    video_url.append(img['download_url_list'][0])

            data = VedioDetail(
                id=vid,
                desc=desc,
                author=aud,
                video=video_url,
                mp3=mp3,
                video_thum=v_p
            )

            return data


async def main():
    dy = DyVedio()
    vid = await dy.getVedioID("https://v.douyin.com/icjjVJV/")
    if vid:
        await dy.reqAPI(vid)


@logger.catch
def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
