from pathlib import Path

import nonebot
from nonebot import get_driver

from .config import Config

from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name="夏目带笨蛋们疯狂图计划",
    description="夏目老师到 1w 分一定就能带我们疯狂图了，大伙儿加油啊！！！",
    usage="",
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)
