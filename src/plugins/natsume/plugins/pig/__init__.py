from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
from pathlib import Path
from nonebot.log import logger
from random import randint
from ... import config, AccountConfig


__plugin_meta__ = PluginMetadata(
    name="夏目🐖",
    description="夏目在“笨蛋集中营”里发消息就跟上猪猪表情包（但是现在被黑了，猪头变成开发者了 qwq)",
    usage="自动",
)

last_time = [0 for _ in range(len(config.GROUP_AND_USER))]
delay_time = 3*60*60


def is_natsume_and_bendan_group(event: GroupMessageEvent):
    global last_time

    pair = AccountConfig(gin=event.group_id, uin=event.user_id)

    try:
        idx = config.GROUP_AND_USER.index(pair)
    except ValueError:
        return

    if event.time - last_time[idx] > delay_time:
        logger.info(f"idx={idx}, time={event.time}")
        last_time[idx] = event.time
        return True
    else:
        logger.info(
            f"idx={idx}, time={event.time}, delta={event.time-last_time[idx]}")

    return False


img_path = Path('resources/images/buy_pig.png')

pig_cmd = on_message(
    rule=Rule(is_natsume_and_bendan_group),
    priority=1,
    block=False
)


@pig_cmd.handle()
async def _():
    await pig_cmd.finish(MessageSegment.image(f"https://d2ph5fj80uercy.cloudfront.net/0{randint(1,6)}/cat{randint(1,5000)}.jpg"))
