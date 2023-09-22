from pydantic import BaseModel
from typing import Any

class Config(BaseModel):
    """
    uvicorn config
    """
    bind: str = "0.0.0.0"
    port: int = 8000
    LogLevel: str = "DEBUG"
    worker: int = 2  # 工作线程
    reload: bool = False  # 是否热重载

class OnediveConfig(BaseModel):
    """
    Onedive Config
    """
    

class BaseAPI(BaseModel):
    code: int  # 状态码 200:成功 500:错误
    msg: str = None  # 信息（如果有）
    content: Any  # 内容
