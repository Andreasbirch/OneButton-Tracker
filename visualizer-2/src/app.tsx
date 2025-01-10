import React, { useState } from 'react';
import { ipcRenderer } from 'electron';
import Devices from './components/devices/devices';
import Calendar from './components/calendar/Calendar';

ipcRenderer.send('send-message', 'ping');

function App() {
    // const [deviceSelected, setDeviceSelected] = useState(false);
    const [selectedDeviceId, setSelectedDeviceId] = useState<string>(null);
    function handleDeviceSelected(deviceId:string) {
        setSelectedDeviceId(deviceId);
    }

    return <>
        {
            selectedDeviceId ? <Calendar selectedDeviceId={selectedDeviceId} ></Calendar> : <Devices handleDeviceSelected={handleDeviceSelected}></Devices>
        }
    </>
}

export default App;