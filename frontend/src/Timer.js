import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, CircularProgress, CircularProgressLabel } from '@chakra-ui/react'
import axios from 'axios';


function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
};

function Progress({ timeLeft, totalTime}) {
  const percentage = ((totalTime - timeLeft) / totalTime) * 100; // gives us a share of passed time

  return (
    <ChakraProvider>
      <Box p={4}>
        <CircularProgress value={percentage} size="240px" thickness="12px" color="cyan.400">
          <CircularProgressLabel>{formatTime(timeLeft)}</CircularProgressLabel>
        </CircularProgress>
      </Box>
    </ChakraProvider>
  )
}

function Timer() {
  const [timerStatus, setTimerStatus] = useState('stopped');
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const totalTime = 25 * 60;

  useEffect(() => {
    const fetchTimerStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/timer_state');
        const {status, timeLeft} = response.data;
        if (typeof timeLeft === 'number' && !isNaN(timeLeft)) {
          setTimerStatus(status);
          setTimeLeft(timeLeft);
        } else {
          console.error('Invalid data format:', response.data);
        }
        setTimerStatus(status);
        setTimeLeft(timeLeft);
      } catch(error) {
        console.error('Error fetching timer status:', error);
      }
    };
    fetchTimerStatus();

    const interval = setInterval(fetchTimerStatus, 1000); // Fetch every 1 second

    return () => clearInterval(interval); // Cleanup on component unmount
  }, []); /*we pass the empty array to tell react that this component does not depend on any props values, so that when they change
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
      setTimerStatus('pause');
      await axios.post('http://localhost:8000/pause');
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

  return (
    <div className='App'>
      <div className='header'>
        <h1>Pomodoro Timer</h1>
      </div>
      <div className="timer-info">
        <div>Status: {timerStatus}</div>
      </div>
      <Progress timeLeft={timeLeft} totalTime={totalTime}/>
      <div className="buttons">
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
    </div>
  );
}

export default Timer;