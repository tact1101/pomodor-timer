from pydantic import BaseModel
import asyncio


class TimerSettings(BaseModel):
    session_time: int
    break_time: int

# DEFAULT TIMER SETTINGS
DEFAULT_WORK_TIME = 25 * 60  # 25 minutes
DEFAULT_BREAK_TIME = 10 * 60  # 10 minutes
SESSIONS = 4

class TimerState:
    """
    Timer has distinct states: 'work', 'break', 'paused', 'finished'
    The timer transitions between these states based on time_left and break_interval.
    """
    def __init__(self):
        self.timer_status = 'stopped'
        self.default_session_time = DEFAULT_WORK_TIME
        self.default_break_time = DEFAULT_BREAK_TIME
        self.time_left = self.default_session_time
        self.break_interval = self.default_break_time 
        self.interval_task = None
        self.break_task = None
        self.sessions = SESSIONS
        self.current_session = 0
        
    async def countdown_timer(self) -> None:
        while self.current_session < self.sessions:
            print(f"{self.current_session}/{self.sessions} sessions.")
            if self.timer_status == 'work':
                await self._run_work_timer()
            elif self.timer_status == 'break':
                await self._run_break_timer()
            else:
                while self.timer_status == 'paused':
                    await asyncio.sleep(1500)  # If paused just wait
            
        self.timer_status = "finished"

    async def _run_work_timer(self):
        while self.time_left > 0:
            if self.timer_status == "paused":
                await asyncio.sleep(1500)
                continue
            await self._decrement_timer()
        self.timer_status = "break"
        await self._handle_timer_end()
        self.current_session += 1

    async def _run_break_timer(self):
        while self.break_interval > 0:
            if self.timer_status == "paused":
                await asyncio.sleep(1500)
                continue
            await self._decrement_break()
        self.timer_status = "work"
        self.time_left = self.default_session_time
        self.break_interval = self.default_break_time

    async def _decrement_timer(self):
        self.time_left -= 1
        await asyncio.sleep(1)
        print(f"Time left: {self.time_left}")

    async def _decrement_break(self):
        self.break_interval -= 1
        await asyncio.sleep(1)
        print(f"Break time left: {self.break_interval}")

    async def _handle_timer_end(self):
        print(f"Session {self.current_session + 1} complete, starting break.")

    def set_custom_times(self, session_time: int, break_time: int):
        self.default_session_time = session_time
        self.default_break_time = break_time
        self.time_left = session_time
        self.break_interval = break_time
        self.timer_status = "stopped"

    def set_default(self):
        self.default_session_time = DEFAULT_WORK_TIME
        self.default_break_time = DEFAULT_BREAK_TIME
        self.time_left = DEFAULT_WORK_TIME
        self.break_interval = DEFAULT_BREAK_TIME
    
    def start_timer(self):
        if self.timer_status != "work":
            self.timer_status = "work"
            self.interval_task = asyncio.create_task(self.countdown_timer())
        else:
            print("Timer is already running.")
            
    def restart_timer(self):
        pass

timer_state = TimerState()
