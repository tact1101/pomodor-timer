import React, { useState, useEffect } from 'react';
import { 
  Box, 
  CircularProgress, 
  CircularProgressLabel, 
  Button, 
  Input,
  FormLabel,
  FormControl,
  FormHelperText,

} from '@chakra-ui/react';
import axios from 'axios';


function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
};

function CustomTimeForm({ onSubmit }) {
  const [sessionTime, setSessionTime] = useState('');
  const [breakTime, setBreakTime] = useState('');
  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit({ session_time: parseInt(sessionTime) * 60, break_time: parseInt(breakTime) * 60 });
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormControl>
        <FormLabel>Session time (minutes)</FormLabel>
          <Input
          className='custom-input'
          type="number" 
          value={sessionTime} onChange={(e) => setSessionTime(e.target.value)}
          />
          <FormHelperText>Enter session time</FormHelperText>
        <FormLabel>Break time (minutes)</FormLabel>
          <Input 
          type="number" 
          value={breakTime} 
          onChange={(e) => setBreakTime(e.target.value)}
          />
           <FormHelperText>Enter break time</FormHelperText>
        </FormControl>
      <Button
            mt={4}
            colorScheme='teal'
            type='submit'
            size='sm'
            variant='solid'
          >
            Submit
          </Button>
    </form>
  );
}

function Progress({ timeLeft, totalTime}) {
  const percentage = ((totalTime - timeLeft) / totalTime) * 100; // gives us a share of passed time

  return (
    <Box p={4}>
      <CircularProgress value={percentage} size="240px" thickness="12px" color="cyan.400">
        <CircularProgressLabel>{formatTime(timeLeft)}</CircularProgressLabel>
      </CircularProgress>
    </Box>
  )
}

function Timer() {
  const [timerStatus, setTimerStatus] = useState('stopped');
  const [timeLeft, setTimeLeft] = useState('');
  const [totalTimeCustom, setTotalTimeCustom] = useState('');

  useEffect(() => {
    const fetchTimerStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/timer/timer_state');
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
      await axios.post('http://localhost:8000/timer/start');
      setTimerStatus('work');
    } catch(error) {
      console.error('Error starting timer:', error);
    }
  };

  const pauseTimer = async () => {
    try {
      setTimerStatus('paused');
      await axios.post('http://localhost:8000/timer/pause');
    } catch(error) {
      console.error('Error pausing timer:', error);
    }
  };

  const resetTimer = async () => {
    try {
      await axios.post('http://localhost:8000/timer/reset');
      setTimerStatus('stopped');
      setTimeLeft(totalTimeCustom);
    } catch(error) {
      console.error('Error resetting timer:', error);
    }
  };

  const setCustomTimes = async ({ session_time, break_time}) => {
    try {
      await axios.post("http://localhost:8000/timer/custom_time_session", {
        session_time,
        break_time,
      });
      setTotalTimeCustom(session_time);
      setTimeLeft(session_time);
      setTimerStatus('stopped');
    } catch (error) {
      console.error('Error setting custom time:', error);
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
      <Progress timeLeft={timeLeft} totalTime={totalTimeCustom}/>
      <div className="custom-buttons">
        <Button 
        colorScheme='teal'
        size='sx'
        className='control-button'
        onClick={startTimer} disabled={timerStatus === 'work'}>
          Start
        </Button>
        <Button 
        colorScheme='teal'
        size='sx'
        className='control-button'
        onClick={pauseTimer} disabled={timerStatus !== 'work'}>
          Pause
        </Button>
        <Button 
        colorScheme='teal'
        size='sx'
        className='control-button'
        onClick={resetTimer}>
          Reset
        </Button>
      </div>
      <div className="custom-session-time">
          <CustomTimeForm onSubmit={setCustomTimes} />
      </div>
    </div>
  );
}

export default Timer;