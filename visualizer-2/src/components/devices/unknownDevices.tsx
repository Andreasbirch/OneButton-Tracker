import React from 'react';
import { Button } from 'react-bootstrap';
import { UnknownDevice } from '../../models/patients/PatientDevice';

type UnknownDeviceProps = {
    unknownDevice: UnknownDevice;
    handleDeviceSelected: (selectedDevice: UnknownDevice) => void;
}


function UnknownDeviceComponent({unknownDevice, handleDeviceSelected}: UnknownDeviceProps  ) {

    console.log("Unknown device", unknownDevice);
    return <Button
                size="lg"
                onClick={() => handleDeviceSelected(unknownDevice)}
                style={{
                    backgroundColor: 'lightgray',
                    width: '100%',
                    marginBottom: '20px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '10px 20px'
                }}>
                <span>Add patient</span>
                <span style={{ fontSize: '1.2em' }}>+</span>
                </Button>
}

export default UnknownDeviceComponent;