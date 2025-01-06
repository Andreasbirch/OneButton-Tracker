import React, { useState } from 'react';
import { ipcRenderer } from 'electron';
import { UsbDevice } from './../models/UsbDevice';
import { Drive } from './../models/Drive';

ipcRenderer.send('available-devices-request', '');

function Devices() {
    const [drives, setDrives] = useState<Drive[]>([]);
    const [usbDevices, setUsbDevices] = useState<UsbDevice[]>([]);

    ipcRenderer.on('available-devices-broadcast', (e, args: {drives: Drive[], usbDevices: UsbDevice[]}) => {
        console.log("Received devices from broadcast", args);
        setDrives(args.drives);
        setUsbDevices(args.usbDevices);
    });

    return <>
        {
            (!drives || drives.length === 0) ? <div> no devices found...</div> : drives.map(drive => {
                return <div key={drive.path}>{drive.label} {drive.path}</div>
            })
        }
    </>
}

export default Devices;