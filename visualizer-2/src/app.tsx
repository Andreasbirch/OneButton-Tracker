import React from 'react';
import { ipcRenderer } from 'electron';

ipcRenderer.send('send-message', 'ping');

function App() {
    return <div>
        <h1>React</h1>
    </div>
}

export default App;