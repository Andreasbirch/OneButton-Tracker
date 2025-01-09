import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import { UnknownOBTDevice } from '../../models/UnknownOBTDevice';

type UnknownDeviceProps = {
    unknownDevice: UnknownOBTDevice;
    handleDeviceSelected: (selectedDevice: UnknownOBTDevice) => void;
}


function UnknownDevice({unknownDevice, handleDeviceSelected}: UnknownDeviceProps  ) {

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
                <span>{unknownDevice.fullPath}</span>
                <span style={{ fontSize: '1.2em' }}>+</span>
                </Button>
}

export default UnknownDevice;