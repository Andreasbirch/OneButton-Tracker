import React, { useEffect, useState } from 'react';

interface DeviceMapping {
    deviceInfo: any[];
    driveInfo: any[];
}

function Devices() {
    const [devices, setDevices] = useState<string>('No devices connected');
    const [deviceMapping, setDeviceMapping] = useState<DeviceMapping | null>(null);

    // Listen for real-time device updates
    useEffect(() => {
        window.electron.onDeviceUpdate((data: any) => {
            setDevices(data);
        });

        return () => {
            // No cleanup needed as event listener is managed in preload
        };
    }, []);

    // Fetch device mapping on component mount
    useEffect(() => {
        const fetchDeviceMapping = async () => {
            const mapping = await window.electron.getDeviceMapping();
            setDeviceMapping(mapping);
        };

        fetchDeviceMapping();
    }, []);

    return (
        <div>
            <h2>Connected Devices</h2>
            <pre>{devices}</pre>

            <h3>Device Mapping</h3>
            {deviceMapping ? (
                <div>
                    <h4>USB Devices</h4>
                    <pre>{JSON.stringify(deviceMapping.deviceInfo, null, 2)}</pre>

                    <h4>Drives</h4>
                    <pre>{JSON.stringify(deviceMapping.driveInfo, null, 2)}</pre>
                </div>
            ) : (
                <p>Loading device mapping...</p>
            )}
        </div>
    );
};

export default Devices;