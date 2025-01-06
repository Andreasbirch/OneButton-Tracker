import React from 'react';
import { ipcRenderer } from 'electron';

ipcRenderer.send('send-message', 'ping');

function App() {
    return <div>
        <h1>React</h1>
        <button type='button' onClick={() => {
            console.log("Klik registreret");
            ipcRenderer.send('get-usb-devices-request');
            ipcRenderer.on('get-usb-devices-response', (e, data) => {
                console.log("Received data", data);
            });
        }}>Tryk</button>
    </div>
}

export default App;