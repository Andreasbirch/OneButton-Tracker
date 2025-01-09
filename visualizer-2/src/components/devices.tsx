import React, { useEffect, useState } from 'react';
import { ipcRenderer } from 'electron';
import { UsbDevice } from './../models/UsbDevice';
import { UsbDrive } from './../models/UsbDrive';
import { Button, Col, Container, Form, FormGroup, Row } from 'react-bootstrap';
ipcRenderer.send('available-devices-request', '');

function Devices({handleDeviceSelected}: {handleDeviceSelected: () => void}) {
    const [drives, setDrives] = useState<UsbDrive[]>([]);
    const [usbDevices, setUsbDevices] = useState<UsbDevice[]>([]);
    
    useEffect(() => {
        ipcRenderer.on('available-devices-broadcast', (e: Electron.IpcRendererEvent, args: { drives: UsbDrive[], usbDevices: UsbDevice[] }) => {
          console.log("Received devices from broadcast", args);
          setDrives(args.drives);
          setUsbDevices(args.usbDevices);
        });
        ipcRenderer.send('available-devices-request', '');
    }, []); // Empty dependency array ensures this runs once on mount



    return (
        <Container
          fluid
          className="d-flex justify-content-center align-items-center"
          style={{
            height: '100vh',
            backgroundColor: '#f8f9fa'
          }}
        >
          <div
            style={{
              width: '400px',
              textAlign: 'center',
              padding: '30px',
              border: '1px solid #ddd',
              borderRadius: '8px',
              backgroundColor: '#fff',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)'
            }}
          >
            {/* Title */}
            <h2 style={{ marginBottom: '30px' }}>Devices</h2>
            
            {(!drives || drives.length === 0) ? 
                <Button
                variant='secondary'
                size="lg"
                disabled
                style={{
                    width: '100%',
                    marginBottom: '20px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '10px 20px'
                }}
                >
                <span>No devices found.</span>
                </Button> :
                <Button
                size="lg"
                onClick={handleDeviceSelected}
                style={{
                    backgroundColor: '#D44343',
                    width: '100%',
                    marginBottom: '20px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '10px 20px'
                }}
                >
                <span>{drives[0].label}</span>
                <span style={{ fontSize: '1.2em' }}>→</span>
                </Button>
            }
    
            {/* Link */}
            <a
              onClick={handleDeviceSelected}
              href="#"
              style={{
                fontSize: '0.9em',
                textDecoration: 'none',
                color: '#007bff'
              }}
            >
              All patients
            </a>
          </div>
        </Container>
      );











    return <>
        <Container>
            <Row style={{display: 'flex', justifyContent: 'center'}}>
                <Col style={{display: 'flex', justifyContent: 'center'}}>
                    <Form style={{maxWidth: '20%', backgroundColor: '#eee'}}>
                        <FormGroup>
                            <h3>Devices</h3>
                        </FormGroup>
                        <FormGroup>
                            {(!drives || drives.length === 0) ? 
                                <Button 
                                    className='btn btn-primary' 
                                    style={{
                                        minWidth: '100%',
                                        backgroundColor: 'lightgray',
                                        color: '#FFF',
                                        borderRadius: 10
                                    }}></Button> :
                                <Button 
                                    className='btn btn-primary' 
                                    onClick={handleDeviceSelected}
                                    style={{
                                        minWidth: '100%',
                                        backgroundColor: '#D44343',
                                        color: '#FFF',
                                        borderRadius: 10
                                    }}>{drives[0].label}</Button>
                            }
                        </FormGroup>
                    </Form>
                </Col>
            </Row>
        </Container>
        
        <Container>
            <Row>
                <Col style={{display: 'flex'}}>

                
                </Col>
            </Row>
        </Container>
    </>
}

export default Devices;