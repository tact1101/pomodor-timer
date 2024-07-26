from pydantic import BaseModel

class TimerState(BaseModel):
    status: str
    timeLeft: int