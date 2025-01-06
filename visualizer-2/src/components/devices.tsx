import React, { Suspense, useEffect, useState } from 'react';
import { ipcRenderer } from 'electron';

function Devices() {
    const [devices, setDevices] = useState<string[]>([]);

    ipcRenderer.on('available-devices-broadcast', (e, args) => {
        console.log("Received devices from broadcast", args);
        setDevices(args);
    });

    return <>
        {
            (!devices || devices.length === 0) ? <div> no devices found...</div> : devices.map(device => {
                return <div>{device}</div>
            })
        }
    </>
}

export default Devices;