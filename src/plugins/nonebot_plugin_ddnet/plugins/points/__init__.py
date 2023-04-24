from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
from pathlib import Path
from nonebot.log import logger
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg, ArgPlainText
from nonebot.matcher import Matcher
import aiohttp
from urllib.parse import quote
from nonebot.exception import MatcherException
from ... import config



__plugin_meta__ = PluginMetadata(
    name="points",
    description="ddnet.org/players",
    usage="/points 昵称",
)

points_cmd = on_command("points") 

@points_cmd.handle()
async def _(event: Event, matcher: Matcher, arg: Message = CommandArg()):
    if player_name := arg.extract_plain_text():
        matcher.set_arg("player_name", arg)


@points_cmd.got("player_name",prompt="Plz input player name!")
async def _(player_name: str = ArgPlainText()):
    try:
        async with aiohttp.ClientSession() as session:
            logger.info(str(config.points_url + quote(player_name)))
            async with session.get(config.points_url + quote(player_name)) as response:
                json = await response.json()
                if json:
                    await points_cmd.finish("# {player_name}\n分数: {points};\n排名: {rank}.".format(**json["points"], player_name=player_name))
                else:
                    await points_cmd.finish(f"player {player_name} cannot be found.")
    except MatcherException:
        raise
    except Exception as e:
        await points_cmd.finish(str(e))