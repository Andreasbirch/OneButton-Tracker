import React, { useState } from 'react';
import { ipcRenderer } from 'electron';
import Devices from './components/devices/devices';
import Calendar from './components/calendar/Calendar';

ipcRenderer.send('send-message', 'ping');

function App() {
    const [deviceSelected, setDeviceSelected] = useState(false);
    function handleDeviceSelected() {
        setDeviceSelected(true);
    }

    return <>
        {
            deviceSelected ? <Calendar></Calendar> : <Devices handleDeviceSelected={handleDeviceSelected}></Devices>
        }
    </>
}

export default App;