import React from 'react';
import { Button } from 'react-bootstrap';
import { PatientDevice } from '../../models/patients/PatientDevice';

type KnownDeviceProps = {
    patientDevice: PatientDevice;
    handleDeviceSelected: () => void;
}

function KnownDevice({patientDevice, handleDeviceSelected}: KnownDeviceProps  ) {
    return <Button
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
                }}>
                <span>{patientDevice.patientName}</span>
                <span style={{ fontSize: '1.2em' }}>→</span>
                </Button>
}

export default KnownDevice;