import React from 'react';
import { ipcRenderer } from 'electron';
import Devices from './components/devices';

ipcRenderer.send('send-message', 'ping');

function App() {
    return <>
        <Devices></Devices>
    </>
}

export default App;