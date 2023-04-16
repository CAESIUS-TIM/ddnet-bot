from pathlib import Path

import nonebot
from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="ddnet",
    description="ddnet api 小工具集",
    usage="",
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

