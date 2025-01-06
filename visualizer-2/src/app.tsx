import React from 'react';
const { ipcRenderer } = window.require('electron');

ipcRenderer.send('anything-asynchronous', 'ping');

function App() {
    return <div>
        <h1>React</h1>
    </div>
}

export default App;