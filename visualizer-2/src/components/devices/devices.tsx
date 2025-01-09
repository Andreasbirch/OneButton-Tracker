import React, { useEffect, useState } from 'react';
import { ipcRenderer } from 'electron';
import { Button, Col, Container, Form, FormGroup, Row } from 'react-bootstrap';
import KnownDevice from './knownDevices';
import { PatientDevice, UnknownDevice } from '../../models/patients/PatientDevice';
import UnknownDeviceComponent from './unknownDevices';
ipcRenderer.send('available-devices-request', '');

function Devices({handleDeviceSelected}: {handleDeviceSelected: () => void}) {
    const [patientDevice, setPatientDevice] = useState<PatientDevice[]>([]);
    const [unknownDevices, setUnknownDevices] = useState<UnknownDevice[]>([]);
    const [selectedDevice, setSelectedDevice] = useState<UnknownDevice | null>(null);
    const [isFormVisible, setIsFormVisible] = useState(false);
    const [patientName, setPatientName] = useState<string>(''); // State for capturing the user name

    useEffect(() => {
        ipcRenderer.on('available-devices-broadcast', (e: Electron.IpcRendererEvent, args: { patientDevices: PatientDevice[], unknownDevices: UnknownDevice[] }) => {
          console.log("Received devices from broadcast", args);
          setPatientDevice(args?.patientDevices?? []);
          setUnknownDevices(args?.unknownDevices?? []);
          console.log(patientDevice, unknownDevices);
        });
        ipcRenderer.send('available-devices-request', '');
    }, []); // Empty dependency array ensures this runs once on mount
    useEffect(() => {
       console.log(unknownDevices);
    }, [unknownDevices]);


    const handleUnknownDeviceClick = (device: UnknownDevice) => {
        setSelectedDevice(device);
        setIsFormVisible(true); // Show the form when an unknown device is clicked
    };

    const handleBackClick = () => {
        setIsFormVisible(false); // Go back to the device list view
        setSelectedDevice(null);
    };

    const handleCreateClick = () => {
        if (selectedDevice) {
            ipcRenderer.invoke('create-device', selectedDevice, patientName).then(() => {
                handleBackClick();
            });
        }
    };

    const isEmptyDeviceList = patientDevice.length === 0 && unknownDevices.length === 0;

    return (
        <Container
          fluid
          className="d-flex justify-content-center align-items-center"
          style={{
            height: '100vh',
            backgroundColor: '#f8f9fa'
          }}>
          <div
            style={{
              width: '400px',
              textAlign: 'center',
              padding: '30px',
              border: '1px solid #ddd',
              borderRadius: '8px',
              backgroundColor: '#fff',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)'
            }}>
            {isFormVisible ? (
                    // Form for creating a new device
                    <>
                        <h2 style={{ marginBottom: '30px' }}>Create Device</h2>
                        {selectedDevice && (
                            <Form>
                                <FormGroup as={Row} controlId="deviceId">
                                    <Form.Label column sm={4}>Device ID</Form.Label>
                                    <Col sm={8}>
                                        <Form.Control
                                            type="text"
                                            value={selectedDevice.id}
                                            readOnly
                                        />
                                    </Col>
                                </FormGroup>
                                <FormGroup as={Row} controlId="devicePath">
                                    <Form.Label column sm={4}>Device Path</Form.Label>
                                    <Col sm={8}>
                                        <Form.Control
                                            type="text"
                                            value={selectedDevice.devicePath}
                                            readOnly
                                        />
                                    </Col>
                                </FormGroup>
                                <FormGroup as={Row} controlId="patientName">
                                    <Form.Label column sm={4}>Patient Name</Form.Label>
                                    <Col sm={8}>
                                        <Form.Control
                                            type="text"
                                            placeholder="Enter patient name"
                                            value={patientName}
                                            onChange={(e) => setPatientName(e.target.value)}
                                        />
                                    </Col>
                                </FormGroup>
                                <Button
                                    variant="primary"
                                    onClick={handleCreateClick}
                                    style={{ marginTop: '20px' }}
                                >
                                    Create
                                </Button>
                                <Button
                                    variant="secondary"
                                    onClick={handleBackClick}
                                    style={{ marginLeft: '10px', marginTop: '20px' }}
                                >
                                    Back
                                </Button>
                            </Form>
                        )}
                    </>
                ) : (
                    // Device list view
                    <>
                        <h2 style={{ marginBottom: '30px' }}>Devices</h2>
                        {isEmptyDeviceList ? (
                            <p>No devices found.</p> // Show this message if no devices are found
                        ) : (
                            <>
                                {patientDevice?.map((d, i) => (
                                    <KnownDevice 
                                        key={`${i} ${d.id}`} 
                                        patientDevice={d} 
                                        handleDeviceSelected={() => {}} />
                                ))}
                                {unknownDevices?.map((d,i) => (
                                    <UnknownDeviceComponent
                                        key={`${i} ${d.id}`}
                                        unknownDevice={d}
                                        handleDeviceSelected={() => handleUnknownDeviceClick(d)}
                                    />
                                ))}
                            </>
                        )}
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
                    </>
                )}
          </div>
        </Container>
      );
}

export default Devices;