import React from 'react';
import './App.css';
import Timer from './Timer';
import { ChakraProvider } from '@chakra-ui/react';

function App() {
  return (
    <ChakraProvider>
      <div className="App">
        <Timer />
      </div>
    </ChakraProvider>
  );
}

export default App;