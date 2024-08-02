from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 구체적인 오리진으로 변경하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# 알람 데이터를 저장할 간단한 in-memory 저장소
alarms = {}

class AlarmSettings(BaseModel):
    bed_time: str
    wake_up_time: str

class SnoozeSettings(BaseModel):
    current_time: str
    snooze_duration: int = 5

@app.post("/set_alarm")
async def set_alarm(settings: AlarmSettings):
    try:
        optimal_time = await get_optimal_alarm_time(settings.bed_time, settings.wake_up_time)
        store_alarm(optimal_time)
        return {"message": "Alarm set successfully", "optimal_time": optimal_time}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop_alarm")
async def stop_alarm():
    # 실제 구현에서는 현재 시간과 가장 가까운 알람을 찾아 중지해야 합니다.
    return {"message": "Alarm stopped"}

@app.post("/snooze_alarm")
async def snooze_alarm_endpoint(settings: SnoozeSettings):
    try:
        new_alarm_time = snooze_alarm(settings.current_time, settings.snooze_duration)
        return {"message": f"Alarm snoozed for {settings.snooze_duration} minutes", "new_alarm_time": new_alarm_time}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/alarms")
async def get_alarms_endpoint():
    return alarms

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

async def get_optimal_alarm_time(bed_time: str, wake_up_time: str) -> str:
    prompt = PromptTemplate(
        input_variables=["bed_time", "wake_up_time"],
        template="Based on bedtime {bed_time} and wake up time {wake_up_time}, what's the optimal alarm time? Please respond with just the time in HH:MM format."
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    optimal_time = chain.run(bed_time=bed_time, wake_up_time=wake_up_time)
    return optimal_time.strip()

def store_alarm(alarm_time: str):
    alarms[alarm_time] = {
        "original_time": alarm_time,
        "current_time": alarm_time,
        "snoozed": False
    }

def snooze_alarm(current_time: str, snooze_duration: int) -> str:
    if not alarms:
        raise ValueError("No active alarm found")

    current_time_obj = datetime.strptime(current_time, "%H:%M")
    
    closest_alarm = min(alarms.keys(), key=lambda x: abs(datetime.strptime(x, "%H:%M") - current_time_obj))
    
    new_alarm_time = (current_time_obj + timedelta(minutes=snooze_duration)).strftime("%H:%M")
    alarms[new_alarm_time] = {
        "original_time": alarms[closest_alarm]["original_time"],
        "current_time": new_alarm_time,
        "snoozed": True
    }
    del alarms[closest_alarm]
    return new_alarm_time

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)