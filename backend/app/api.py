from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .models import TimerState
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define the CORS origins
origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get route
@app.get("/", tags=["root"])
def read_root() -> dict:
    return {"message": "FastAPI is running!"}

timer_status = 'stopped'
timeLeft = 25 * 60 # 25 minutes (default) in seconds
interval = None # default

# Timer has 3 states: running, paused, finished
# Timer can be started, stopped, resumed, finished
# We make post requests with FastAPI and fetch them on the JS side

async def countdown_timer():
    global timeLeft, timer_status
    while True:
        if timer_status == 'running' and timeLeft > 0:
            timeLeft -= 1
            await asyncio.sleep(1) # wait for 1 second before decrementing the timeLeft
            print(f"Time left: {timeLeft}")
        elif timeLeft == 0:
            timer_status = "finished"
            break
        else: 
            # If nothing from above meets the conditions, we hand over control to the main flow of the program
            await asyncio.sleep(0.1)

@app.get("/api/hello")
async def read_root():
    return {"message": "Hello World"}

@app.post("/start")
async def start_timer():
    global timer_status, interval
    if timer_status != "running":
        timer_status = "running" # change the timer state
        interval = asyncio.create_task(countdown_timer())
    return TimerState(status=timer_status, timeLeft=timeLeft)

@app.post("/pause")
async def pause_timer():
    global timer_status
    if timer_status == "running":
        timer_status = "paused"
    return TimerState(status=timer_status, timeLeft=timeLeft)

@app.post("/reset")
async def reset_timer():
    global timer_status, timeLeft, interval 
    timeLeft = 25 * 60 # update the timeLeft
    timer_status = "stopped"
    if interval:        # if timer runs, we cancel it
        interval.cancel()
    return TimerState(status=timer_status, timeLeft=timeLeft)

@app.get("/timer_state")
async def get_timer_state():
    global timer_status, timeLeft
    return TimerState(status=timer_status, timeLeft=timeLeft)
