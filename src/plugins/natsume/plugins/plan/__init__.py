""" 每日早安 """
from dataclasses import asdict

from nonebot import get_bot
from nonebot.adapters import Message, Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v11 import Message as V11Message, MessageSegment as V11MessageSegment
from nonebot.log import logger
from nonebot.params import CommandArg, Depends
from nonebot.plugin import PluginMetadata, on_command
from nonebot_plugin_apscheduler import scheduler
from nonebot import get_bot
from ... import config
import requests

__plugin_meta__ = PluginMetadata(
    name="每日查夏目分",
    description="助力夏目老师1w查分计划",
    usage="""每天早晨查夏目分""",
    extra={
        "adapters": ["OneBot V11"],
    },
)

from pathlib import Path
img_path = Path('resources/images/flower_pig.jpg')

import json
import os
from json import JSONDecodeError
file_name = "natsume.json"
last_points = None
try:
    if os.path.exists(file_name):
        with open(file_name,"r",encoding="utf-8") as f:
            json_obj = json.load(f)
            logger.info(f"json_obj: {json_obj}")
            if isinstance(json_obj, dict):
                last_points = json_obj.get("last_points")
    else:
        logger.info("未初始化")
        
except JSONDecodeError as e:
    logger.error("JSON文件解码错误(数据格式不正确|没有内容)")

@scheduler.scheduled_job(
    "cron",
    hour=config.morning_time.hour,
    minute=config.morning_time.minute,
    second=config.morning_time.second,
    id="morning",
)
async def points_natsume():
    global last_points
    bot = get_bot()
    if isinstance(bot, V11Bot):

        for i in range(5):
            resp = requests.get("https://ddnet.org/players/?json2=夏目夏至日")
            if resp.status_code == 200:
                break
        json_obj = None
        if resp.status_code == 200:
            json_obj = resp.json()
            
        if json_obj:
            points = json_obj["points"]["points"]
        else:
            logger.error("查不到夏目老师的分 qwq")
            return

        logger.info(f"夏目分数 {points}")
        if last_points:
            message = f"夏目老师今天已经 {points} 了，相比昨天增加了 {points - last_points}"
        else:
            message = f"夏目老师今天已经 {points} 了"
        for i in config.GROUP_AND_USER:
            await bot.send_group_msg(group_id=i.gin,message= V11Message(V11MessageSegment.text(message+"\n")+V11MessageSegment.image(img_path)))
        last_points = points
        with open(file_name,"w+",encoding="utf-8") as f:
            f.write(json.dumps({"last_points":last_points}, ensure_ascii=False))
