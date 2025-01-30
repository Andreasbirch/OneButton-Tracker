import { Drive } from 'drivelist/js';
import fs from 'fs';
import path from 'path';
import { IDeviceService as IDeviceService } from './IDeviceService';
import { PatientDevice, UnknownDevice } from '../models/patients/PatientDevice';
import { PatientRepository } from './PatientRepository';
const usb = require('usb');
const driveList = require('drivelist');


export class DeviceService implements IDeviceService{
    handleDeviceConnected = async ():Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }> => {
        return this.getAvailableDevices();
    };
  
    handleDeviceDisconnected = async ():Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }>  => {
        return this.getAvailableDevices();
    };
    
    private patientManager = new PatientRepository();
    private webusb = new usb.WebUSB({ allowAllDevices: true });

    public getAvailableDevices = async ():Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }> => {
        console.log("GetAvailableDevices");
        // Get usb devices
        let _usbDevices = await this.webusb.getDevices();
        console.log("_usbDevices", _usbDevices);

        let usbDevices: {serialNumber: string, vendorId: number, productId: number}[] = _usbDevices.map((device: any) => ({
            serialNumber: device.serialNumber,
            vendorId: device.vendorId,
            productId: device.productId
        }));
        
        if(!usbDevices || usbDevices.length === 0)
            return {patientDevices: [], unknownDevices: []};

        // Try and get usb drives
        let drives: Drive[] = [];
        let attempts = 60;
        for (let attempt = 0; attempt < attempts; attempt++) {
            console.log(`-----${attempt}-----`);

            let _drives = await driveList.list();
            await new Promise(resolve => setTimeout(resolve, 250)); //Sleep .25 sec
            if(!_drives)
                continue;
            
            let _usbDrives = _drives.filter((o:Drive) => o.isUSB);
            console.log(`${_usbDrives.length}/${usbDevices.length}`);
            if(_usbDrives.length != usbDevices.length)
                continue;

            let allMountPoints = _usbDrives.every((o:Drive) => o.mountpoints.length > 0)
            console.log(allMountPoints);
            if(!allMountPoints)
                continue;   



            drives = _drives;
            break;
            // console.log(attempt, .map((o:Drive) => o.mountpoints));
            // if(_drives && _drives.filter((d:Drive) => d.isUSB).length === usbDevices.length && _drives.filter((d:Drive) => d.isUSB).every((d:Drive) => d.mountpoints.length > 0)) {
            //     drives = _drives;
            //     break;
            // }
        }

        if (!drives || drives.length === 0)
            return {patientDevices: [], unknownDevices: []};

        const usbDrives = drives.filter(drive => drive.isUSB);
        if (drives.length === 0)
            return {patientDevices: [], unknownDevices: []};
        console.log(usbDrives);

        const obtDevices: UnknownDevice[] = usbDrives.map(drive => {
            const mountpoint = drive.mountpoints[0];
            console.log("--Mountpoints", drive, drive.mountpoints, drive.mountpoints[0]);
            const dir = fs.readdirSync(mountpoint?.path);

            console.log(drive, dir);
            if (!dir || dir.length === 0)
                return null;
    
            const matchingDevice = usbDevices.find(d => dir.some(o => path.parse(o).name === `.OBT${d.serialNumber}`));
            console.log("matchingDevice", matchingDevice);
            if (!matchingDevice)
                return null;
    
            return {
                id: matchingDevice.serialNumber,
                devicePath: path.basename(mountpoint.path),
                fullPath: mountpoint.path
            };
        }).filter(o => o);
        console.log("OBTDevices", obtDevices);
        
        const patientDeviceMap = this.patientManager.getPatientDeviceMap();
        const patientDevices: PatientDevice[] = obtDevices.map(o => Object.values(patientDeviceMap).find(m => m.id === o.id)).filter(o => o);
        console.log("patientDeviceMap", patientDeviceMap);
        console.log("patientDevices", patientDevices);
        return { patientDevices, unknownDevices: obtDevices.filter(o => !Object.values(patientDeviceMap).some(d => d.id === o.id)) };
    }   

  
}
