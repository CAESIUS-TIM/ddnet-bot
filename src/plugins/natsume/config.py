from pydantic import BaseModel, Extra


from datetime import time



class Config(BaseModel, extra=Extra.ignore):
    # 每日早安
    morning_time: time = time(7, 30, 0)
    
    bendan_group_id: int = 789997943
    natsume_user_id: int = 2652334532

