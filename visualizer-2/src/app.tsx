import React, { useState } from 'react';
import { ipcRenderer } from 'electron';
import Devices from './components/devices';

ipcRenderer.send('send-message', 'ping');

function App() {
    const [deviceSelected, setDeviceSelected] = useState(false);
    function handleDeviceSelected() {
        setDeviceSelected(true);
    }
    
    return <>
        {
            deviceSelected ? <></> : <Devices handleDeviceSelected={handleDeviceSelected}></Devices>
        }
    </>
}

export default App;