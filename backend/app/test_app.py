import unittest
from fastapi.testclient import TestClient
from app.api import app, TimerState

class TestTimerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.timer_state = TimerState()
        
    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "FastAPI is running!"})
        
    def test_start_timer(self):
        response = self.client.post("/start")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "running")
        
    def test_pause_timer(self):
        self.client.post("/start")
        response = self.client.post("/reset")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "stopped")
        self.assertEqual(response.json()["timeLeft"], 25 * 60)
    
    
    def test_get_timer_state(self):
        response = self.client.get("/timer_state")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
        self.assertIn("timeLeft", response.json())

if __name__ == "__main__":
    unittest.main()
        