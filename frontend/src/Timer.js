import React, { useState, useEffect } from 'react';
import axios from 'axios';


function Timer() {
  const [timerStatus, setTimerStatus] = useState('stopped');
  const [timeLeft, setTimeLeft] = useState(25 * 60);

  useEffect(() => {
    const fetchTimerStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/timer_state');
        const {status, timeLeft} = response.data;
        console.log('Status:', status, 'Time left:', timeLeft);

        if (typeof time_left === 'number' && !isNaN(timeLeft)) {
          setTimerStatus(status);
          setTimeLeft(timeLeft);
        } else {
          console.error('Invalid data format:', response.data);
        }
        console.log('timeLeft:', timeLeft);
        setTimerStatus(status);
        setTimeLeft(timeLeft);
      } catch(error) {
        console.error('Error fetching timer status:', error);
      }
    };
    fetchTimerStatus();

    const interval = setInterval(fetchTimerStatus, 1000); // Fetch every second

    return () => clearInterval(interval); // Cleanup on component unmount
  }, []); /*we pass the empty array to tell react that this component does not depend on any proprs values, so that when they change
            react won't be doing unnecessary re-fetching and subsequent re-rendering of the component*/

  const startTimer = async () => {
    try {
      await axios.post('http://localhost:8000/start');
      setTimerStatus('running');
    } catch(error) {
      console.error('Error starting timer:', error);
    }
  };

  const pauseTimer = async () => {
    try {
      await axios.post('http://localhost:8000/pause');
      setTimerStatus('pause');
    } catch(error) {
      console.error('Error pausing timer:', error);
    }
  };

  const resetTimer = async () => {
    try {
      await axios.post('http://localhost:8000/reset');
      setTimerStatus('stopped');
      setTimeLeft(25 * 60);
    } catch(error) {
      console.error('Error resetting timer:', error);
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
  };

  return (
    <div className='App'>
      <h1>Pomodoro Timer</h1>
      <div>Status: {timerStatus}</div>
      <div>Time left: {formatTime(timeLeft)}</div>
      <button onClick={startTimer} disabled={timerStatus === 'running'}>
        Start
      </button>
      <button onClick={pauseTimer} disabled={timerStatus !== 'running'}>
        Pause
      </button>
      <button onClick={resetTimer}>
        Reset
      </button>
    </div>
  );
}

export default Timer;