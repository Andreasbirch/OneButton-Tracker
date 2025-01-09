import { Drive } from 'drivelist/js';
import fs from 'fs';
import path from 'path';
import { UsbDevice } from '../models/UsbDevice';
import { UnknownOBTDevice } from '../models/UnknownOBTDevice';
import { Patient } from '../models/Patient';
import driveList from 'drivelist';
import usb from 'usb';

export type IDeviceManager = {
  handleDeviceConnected: () => Promise<{patientData: Patient[]; unknownDrives: UnknownOBTDevice[]}>;

}

export class DeviceManager implements IDeviceManager{
  private static webusb = new usb.WebUSB({ allowAllDevices: true });

  static async getAvailableUSBDevices(): Promise<UsbDevice[]> {
    const usbDevices = await this.webusb.getDevices();
    return usbDevices.map((device: any) => ({
      serialNumber: device.serialNumber,
      vendorId: device.vendorId,
      productId: device.productId
    }));
  }

  static async getAvailableUSBDrives(drives: Drive[], devices: UsbDevice[]): Promise<{patientData: Patient[]; unknownDrives: UnknownOBTDevice[]}> {
    if (!drives || !devices || drives.length === 0 || devices.length === 0)
      return null;

    const usbDrives = drives.filter(drive => drive.isUSB);
    if (usbDrives.length === 0)
      return null;

    const obtDevices = usbDrives.map(drive => {
      const mountpoint = drive.mountpoints[0];
      const dir = fs.readdirSync(mountpoint.path);
      if (!dir || dir.length === 0) return null;

      const matchingDevice = devices.find(d => dir.some(o => path.parse(o).name === `.OBT${d.serialNumber}`));
      if (!matchingDevice) return null;

      return {
        deviceId: matchingDevice.serialNumber,
        devicePath: path.basename(mountpoint.path),
        fullPath: mountpoint.path
      };
    }).filter(o => o);

    const deviceMap: Patient[] = obtDevices.map(o => {
      let found = deviceMap.find(m => m.metaData.deviceId === o.deviceId);
      if (!found) return null;
      return found;
    }).filter(o => o);

    return { patientData: deviceMap.map(o => o.metaData), unknownDrives: obtDevices.filter(o => !deviceMap.some(d => d.metaData.deviceId === o.deviceId)) };
  }

  static handleDeviceConnected() {
    // Device connection handling logic goes here...
  }
  handleDeviceConnected: () => Promise<{patientData: Patient[]; unknownDrives: UnknownOBTDevice[]}>;
}
