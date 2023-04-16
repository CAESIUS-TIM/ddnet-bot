from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    points_url : str = "https://ddnet.org/players/?json2="
