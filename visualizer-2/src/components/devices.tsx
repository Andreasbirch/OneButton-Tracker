import React, { useEffect, useState } from 'react';
import { ipcRenderer } from 'electron';
import { UsbDevice } from './../models/UsbDevice';
import { Drive } from './../models/Drive';
import { Button, Col, Container, Row } from 'react-bootstrap';
ipcRenderer.send('available-devices-request', '');

function Devices() {
    const [drives, setDrives] = useState<Drive[]>([]);
    const [usbDevices, setUsbDevices] = useState<UsbDevice[]>([]);

     useEffect(() => {
        const handleAvailableDevices = (e: Electron.IpcRendererEvent, args: { drives: Drive[], usbDevices: UsbDevice[] }) => {
            console.log("Received devices from broadcast", args);
            setDrives(args.drives);
            setUsbDevices(args.usbDevices);
        };
        ipcRenderer.on('available-devices-broadcast', handleAvailableDevices);
        ipcRenderer.send('available-devices-request', '');
        

    }, []); // Empty dependency array ensures this runs once on mount

    return <>
        <Container>
            <Row>
                <Col>
                {(!drives || drives.length === 0) ? 
                    <Button className='btn btn-primary' style={{
                        backgroundColor: 'lightgray',
                        color: '#FFF',
                        borderRadius: 10
                    }}></Button> :
                    <Button className='btn btn-primary' style={{
                        backgroundColor: '#D44343',
                        color: '#FFF',
                        borderRadius: 10
                    }}>{drives[0].label}</Button>
                }
                </Col>
            </Row>
        </Container>
    </>
}

export default Devices;