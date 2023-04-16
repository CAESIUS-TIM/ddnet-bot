""" 每日早安 """
from dataclasses import asdict

from nonebot import get_bot
from nonebot.adapters import Message, Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v11 import Message as V11Message
from nonebot.log import logger
from nonebot.params import CommandArg, Depends
from nonebot.plugin import PluginMetadata, on_command
from nonebot_plugin_apscheduler import scheduler
from nonebot import get_bot
from .. import config
import requests

__plugin_meta__ = PluginMetadata(
    name="每日查夏目分",
    description="助力夏目老师1w查分计划",
    usage="""每天早晨查夏目分""",
    extra={
        "adapters": ["OneBot V11"],
    },
)

natsume_points = -1

@scheduler.scheduled_job(
    "cron",
    hour=config.morning_time.hour,
    minute=config.morning_time.minute,
    second=config.morning_time.second,
    id="morning",
)
async def points_natsume():
    global natsume_points
    bot = get_bot()
    if isinstance(bot, V11Bot):

        for i in range(5):
            resp = requests.get("https://ddnet.org/players/?json2=夏目夏至日")
            if resp.status_code == 200:
                break
        json = None
        if resp.status_code == 200:
            json = resp.json()
            
        if json:
            if natsume_points == -1:
                await bot.send_group_msg(group_id=config.bendan_group_id,message=f"夏目老师今天已经 {json['points']['points']} 了")
            else:
                await bot.send_group_msg(group_id=config.bendan_group_id,message=f"夏目老师今天已经 {json['points']['points']} 了，相比昨天增加了 {json['points']['points'] - natsume_points}")
            natsume_points = json['points']['points']
    logger.info("查夏目分")
