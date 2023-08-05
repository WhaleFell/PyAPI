# onedrive utils
# ref: https://learn.microsoft.com/zh-cn/onedrive/developer/?view=odsp-graph-online
# ref: https://learn.microsoft.com/zh-cn/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online
# 换用 https://login.microsoftonline.com
# https://massivescale.com/microsoft-v2-endpoint-primer/
# https://stackoverflow.com/questions/43810200/microsoft-onedrive-api-invalidauthenticationtoken-compacttoken-parsing-failed-wi#:~:text=You%27re%20authenticating%20against%20the%20wrong%20endpoint.%20The%20login.live.com,code%20provided%20should%20give%20you%20everything%20you%20need.
import httpx
from log import logger
import urllib.parse
import asyncio
from typing import Dict
from pathlib import Path

UA = "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36"


class OnedriveSDK(object):
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = "http://localhost/") -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "Files.Read Files.ReadWrite Files.Read.All Files.ReadWrite.All offline_access"
        self.refresh_token: str = ""
        self.access_token: str = ""
        self.header: dict = {
            "User-Agent": UA,
            # "Authorization": "Bearer "+self.access_token,
        }
        self.FILEPATH = Path(__file__).parent.absolute()
        self.refresh_file_path = Path(self.FILEPATH, ".onedriveRefresh")
        self.access_file_path = Path(self.FILEPATH, ".onedriveAccess")
        self.onedrive_api = "https://graph.microsoft.com/v1.0"

    async def init(self):
        if self.refresh_file_path.exists():
            self.refresh_token = self.refresh_file_path.read_text(
                encoding="utf8")
            await self.getTokenByRefreshToken(self.refresh_token)
        else:
            self.generateLoginURL()
            code = input(">> code=")
            await self.getRefreshTokenByCode(code)
            await self.getTokenByRefreshToken(self.refresh_token)

        if not await self.checkAccessTokenStatus():
            raise Exception("Onedrive Token Invaild")

    def generateLoginURL(self) -> str:
        # url = f"https://login.live.com/oauth20_authorize.srf?client_id={self.client_id}&scope={self.scope}&response_type=code&redirect_uri={self.redirect_uri}"
        url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={self.client_id}&scope={self.scope}&response_type=code&redirect_uri={self.redirect_uri}"
        # https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=[APPLICATION ID]&response_type=coderedirect_uri=[REDIRECT URI]&scope=[SCOPE]

        parsed = urllib.parse.urlsplit(url)
        encoded_query = urllib.parse.quote(parsed.query, safe='=&')
        encoded_url = urllib.parse.urlunsplit(
            parsed._replace(query=encoded_query))
        logger.debug(f"Login onedrive url:{encoded_url}")
        return encoded_url

    async def getRefreshTokenByCode(self, code: str) -> Dict[str, str]:
        async with httpx.AsyncClient(headers=self.header) as c:
            data = {
                "client_id": f"{self.client_id}",
                "redirect_uri": f"{self.redirect_uri}",
                "client_secret": f"{self.client_secret}",
                "code": f"{code}",
                "grant_type": "authorization_code"
            }
            # https://login.microsoftonline.com/common/oauth2/v2.0/token
            resp = await c.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=data, headers=self.header)
            # resp = await c.post("https://login.live.com/oauth20_token.srf", data=data, headers=self.header)
            logger.debug(f"get token raw resp:{resp.text}")
            respJs = resp.json()
            access_token = respJs["access_token"]
            refresh_token = respJs["refresh_token"]

            self.saveRefreshTokenInFile(refresh_token)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

    async def getTokenByRefreshToken(self, refresh_token: str) -> Dict[str, str]:
        async with httpx.AsyncClient(headers=self.header) as c:
            data = {
                "client_id": f"{self.client_id}",
                "redirect_uri": f"{self.redirect_uri}",
                "client_secret": f"{self.client_secret}",
                "refresh_token": f"{refresh_token}",
                "grant_type": "refresh_token"
            }
            # https://login.microsoftonline.com/common/oauth2/v2.0/token
            resp = await c.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=data, headers=self.header)
            logger.debug(f"get token raw resp:{resp.status_code}|{resp.text}")
            respJs = resp.json()
            access_token = respJs["access_token"]
            refresh_token = respJs["refresh_token"]
            self.saveAccessTokenInFile(access_token)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

    def saveRefreshTokenInFile(self, refresh_token: str):
        self.refresh_token = refresh_token
        Path(self.refresh_file_path).write_text(refresh_token, encoding="utf8")
        logger.info("refresh_token save!")

    def saveAccessTokenInFile(self, access_token: str):
        self.access_token = access_token
        self.header["authorization"] = "bearer "+self.access_token
        Path(self.access_file_path).write_text(access_token, encoding="utf8")
        logger.info("AccessToken save!")

    async def checkAccessTokenStatus(self) -> bool:
        async with httpx.AsyncClient(headers=self.header) as c:
            resp = await c.get(self.onedrive_api+"/me/drive/root/children")
            if resp.status_code == 401:
                logger.error(f"AccessToken Invaild!:{resp.text}")
                return False
            logger.success("AccessToken Vaild!")
            return True

    # 获取指定目录下的所有文件路径
    async def get_files_in_folder(self, folder_path, file_paths: list):
        api_url = f'https://graph.microsoft.com/v1.0/me/drive/root:{folder_path}:/children?$filter=file ne null'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = httpx.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data)
        for item in data['value']:
            if any(item['name'].endswith(ext) for ext in [".mp4", ".png", ".jpg"]):
                file_paths.append(item['webUrl'])
            elif item.get('folder') is not None:
                self.get_files_in_folder(
                    item['path'], self.access_token, file_paths)


@logger.catch()
async def main():
    ls = []
    od = OnedriveSDK(
        client_id="3c65486c-38c3-4405-aca1-6b99cf8d7d2a",
        client_secret="l2a8Q~oiKhatN11YsUDKwN-DtlyjZFvIJigF3axT"
    )
    await od.init()
    await od.get_files_in_folder("/yellow", ls)
    print(ls)

if __name__ == "__main__":
    asyncio.run(main())
