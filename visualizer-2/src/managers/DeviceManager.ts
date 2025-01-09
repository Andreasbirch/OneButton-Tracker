import { Drive } from 'drivelist/js';
import fs from 'fs';
import path from 'path';
import { UsbDevice } from '../models/UsbDevice';
import { IDeviceManager } from './IDeviceManager';
import { PatientDevice, UnknownDevice } from '../models/patients/PatientDevice';
import { PatientManager } from './PatientManager';
const usb = require('usb');
const driveList = require('drivelist');


export class DeviceManager implements IDeviceManager{
    handleDeviceConnected = async ():Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }> => {
        return this.getAvailableDevices();
    };
  
    handleDeviceDisconnected = async ():Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }>  => {
        return this.getAvailableDevices();
    };
    
    private patientManager = new PatientManager();
    
    public getAvailableDevices = async ():Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }> => {
        // Get usb devices
        let usbDevices: {serialNumber: string, vendorId: number, productId: number}[] = await this.webusb.getDevices().map((device: any) => ({
            serialNumber: device.serialNumber,
            vendorId: device.vendorId,
            productId: device.productId
        }));
        
        // Try and get usb drives
        let circuitpyDrives: Drive[] = [];
        let attempts = 60;
        for (let attempt = 0; attempt < attempts; attempt++) {
            let _circuitpyDrives = await driveList.list();
            if(_circuitpyDrives &&_circuitpyDrives.length > 0) {
                circuitpyDrives = _circuitpyDrives;
                break;
            }
            
            await new Promise(resolve => setTimeout(resolve, 250)); //Sleep .25 sec
        }

        if (!circuitpyDrives || !usbDevices || circuitpyDrives.length === 0 || usbDevices.length === 0)
            return {patientDevices: [], unknownDevices: []};

        const usbDrives = circuitpyDrives.filter(drive => drive.isUSB);
        if (circuitpyDrives.length === 0)
            return {patientDevices: [], unknownDevices: []};

        const obtDevices: UnknownDevice[] = usbDrives.map(drive => {
            const mountpoint = drive.mountpoints[0];
            const dir = fs.readdirSync(mountpoint.path);
            if (!dir || dir.length === 0) return null;
    
            const matchingDevice = usbDevices.find(d => dir.some(o => path.parse(o).name === `.OBT${d.serialNumber}`));
            if (!matchingDevice) return null;
    
            return {
                id: matchingDevice.serialNumber,
                devicePath: path.basename(mountpoint.path),
                fullPath: mountpoint.path
            };
        }).filter(o => o);
        
        const patientDeviceMap = this.patientManager.getPatientDeviceMap();
        const patientDevices: PatientDevice[] = obtDevices.map(o => Object.values(patientDeviceMap).find(m => m.id === o.id)).filter(o => o);
    
        return { patientDevices, unknownDevices: obtDevices.filter(o => !Object.values(patientDeviceMap).some(d => d.id === o.id)) };
    }   

  private webusb = new usb.WebUSB({ allowAllDevices: true });

  async getAvailableUSBDevices(): Promise<UsbDevice[]> {
    const usbDevices = await this.webusb.getDevices();
    return usbDevices.map((device: any) => ({
      serialNumber: device.serialNumber,
      vendorId: device.vendorId,
      productId: device.productId
    }));
  }
}
