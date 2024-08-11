from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.timer import TimerState, TimerSettings

app = FastAPI()

# Define the CORS origins
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DEFAULT TIMER SETTINGS
DEFAULT_WORK_TIME = 25 * 60  # 25 minutes
DEFAULT_BREAK_TIME = 10 * 60  # 10 minutes
SESSIONS = 4
        

timer_state = TimerState()

@app.get("/", tags=["root"])
def read_root() -> dict:
    return {"message": "FastAPI is running!"}

@app.post("/timer/start")
async def start_timer():
    if timer_state.timer_status != "work":
        timer_state.timer_status = "work"  # change the timer state
        timer_state.interval_task = asyncio.create_task(timer_state.countdown_timer())
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left}

@app.post("/timer/pause")
async def pause_timer():
    if timer_state.timer_status == "work":
        timer_state.timer_status = "paused"
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left}

@app.post("/timer/reset")
async def reset_timer():
    if timer_state.interval_task:
        timer_state.interval_task.cancel()
    timer_state.time_left = timer_state.default_session_time # update the timeLeft
    timer_state.timer_status = "stopped"
    timer_state.break_interval = timer_state.default_break_time # reset break interval
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left}

@app.post("/timer/custom_time_session")
async def set_custom_time_session(settings: TimerSettings):
    timer_state.set_custom_times(settings.session_time, settings.break_time)
    return {"session_time": settings.session_time, "break_time": settings.break_time}

@app.get("/timer/timer_state")
async def get_timer_state():
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left, "breakTime": timer_state.break_interval}