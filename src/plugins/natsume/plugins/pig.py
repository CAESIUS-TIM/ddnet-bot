from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.adapters import Event
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
from pathlib import Path
from nonebot.log import logger
from .. import config


__plugin_meta__ = PluginMetadata(
    name="夏目🐖",
    description="夏目在“笨蛋集中营”里发消息就跟上猪猪表情包",
    usage="自动",
)

def is_natsume_and_bendan_group(event: Event):
    return isinstance(event, GroupMessageEvent) and event.user_id == config.natsume_user_id and event.group_id == config.bendan_group_id

img_path = Path('resources/images/flower_pig.jpg')

pig_cmd = on_message(rule=Rule(is_natsume_and_bendan_group), priority=1, block=False) 

@pig_cmd.handle()
async def _():
    await pig_cmd.finish(MessageSegment.image(r"https://gchat.qpic.cn/gchatpic_new/3587645803/1009631242-2833907660-E5F1EE8DBB32228C7C9264382D30055E/0?term=255&amp;is_origin=0"))