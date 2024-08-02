from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=GOOGLE_API_KEY)

alarms = {}

async def get_optimal_alarm_time(bed_time: str, wake_up_time: str) -> str:
    prompt = PromptTemplate(
        input_variables=["bed_time", "wake_up_time"],
        template="Based on bedtime {bed_time} and wake up time {wake_up_time}, what's the optimal alarm time? Please respond with just the time in HH:MM format."
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    try:
        optimal_time = chain.run(bed_time=bed_time, wake_up_time=wake_up_time)
        return optimal_time.strip()
    except Exception as e:
        raise Exception(f"Failed to get optimal alarm time: {str(e)}")

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

def get_alarms():
    return alarms