from pydantic import BaseModel, Extra


from datetime import time

from enum import IntEnum
from typing import Any, Dict, List, Literal, Optional, Union

from nonebot import get_driver
from nonebot.adapters.onebot.v11.config import Config as OnebotConfig
from pydantic import BaseModel, Field, FilePath, HttpUrl

class AccountConfig(BaseModel):
    gin: int
    uin: int

class Config(BaseModel, extra=Extra.ignore):
    # 每日早安
    morning_time: time = time(12, 00, 0)
    
    GROUP_AND_USER: List[AccountConfig] = Field(default_factory=list, alias="natsume_group_and_user")

