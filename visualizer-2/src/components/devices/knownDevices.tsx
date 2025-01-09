import React from 'react';
import { Button } from 'react-bootstrap';
import { PatientMetaData } from '../../models/Patient';

type KnownDeviceProps = {
    patientData: PatientMetaData;
    handleDeviceSelected: () => void;
}

function KnownDevice({patientData, handleDeviceSelected}: KnownDeviceProps  ) {
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
                <span>{patientData.patientName}</span>
                <span style={{ fontSize: '1.2em' }}>→</span>
                </Button>
}

export default KnownDevice;