from pydantic import BaseModel

class AlarmSettings(BaseModel):
    alarm_time: str
    bed_time: str
    wake_up_time: str

class SnoozeSettings(BaseModel):
    current_time: str
    snooze_duration: int = 5