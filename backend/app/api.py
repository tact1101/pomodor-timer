from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio

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

class TimerState:
    """
    Timer has 3 states: running, paused, finished
    Timer can be started, stopped, resumed, finished
    We make post requests with FastAPI and fetch them on the JS side
    """
    def __init__(self):
        self.timer_status = 'stopped'
        self.time_left = 0.1 * 60  # 25 minutes in seconds
        self.break_interval = 10 * 60  # 10 minutes in seconds
        self.break_time_event = asyncio.Event()
        self.interval_task = None
        self.break_task = None

    async def countdown_timer(self):
        while True:
            if self.timer_status == 'running' and self.time_left > 0:
                self.time_left -= 1
                await asyncio.sleep(1)  # wait for 1 second before decrementing the timeLeft
                print(f"Time left: {self.time_left}")
            elif self.time_left == 0:
                self.timer_status = "finished"
                self.break_time_event.set()
                await self.break_task
                break
            else:
                await asyncio.sleep(1500)

    async def waiter_break_time(self):
        print('...waiting for a break to be set')
        await self.break_time_event.wait()
        print('...set')
        if self.timer_status == "finished":
            while self.break_interval > 0:
                self.break_interval -= 1
                await asyncio.sleep(1)
                print(f"Break time left: {self.break_interval}")
        self.break_time_event.clear()
        

timer_state = TimerState()

@app.get("/", tags=["root"])
def read_root() -> dict:
    return {"message": "FastAPI is running!"}

@app.post("/start")
async def start_timer():
    if timer_state.timer_status != "running":
        timer_state.timer_status = "running"  # change the timer state
        timer_state.interval_task = asyncio.create_task(timer_state.countdown_timer())
        timer_state.break_task = asyncio.create_task(timer_state.waiter_break_time())
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left}

@app.post("/pause")
async def pause_timer():
    if timer_state.timer_status == "running":
        timer_state.timer_status = "paused"
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left}

@app.post("/reset")
async def reset_timer():
    if timer_state.interval_task:
        timer_state.interval_task.cancel()
    if timer_state.break_task:
        timer_state.break_task.cancel()
    timer_state.time_left = 25 * 60  # update the timeLeft
    timer_state.timer_status = "stopped"
    timer_state.break_interval = 10 * 60  # reset break interval
    timer_state.break_time_event.clear()
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left}

@app.get("/timer_state")
async def get_timer_state():
    return {"status": timer_state.timer_status, "timeLeft": timer_state.time_left}
