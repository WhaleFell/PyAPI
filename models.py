from pydantic import BaseModel
from typing import Any


class BaseAPI(BaseModel):
    code: int  # 状态码 200:成功 500:错误
    msg: str = None  # 信息（如果有）
    content: Any  # 内容
