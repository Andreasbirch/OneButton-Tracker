import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { UsbDevice } from './models/UsbDevice';
import { ActivityTypes, Patient, PatientMetaData } from './models/Patient';
import _deviceMap from './data/device_map.json';
import { WebUSBDevice } from 'usb/dist';
import { Drive } from 'drivelist/js';
import fs from 'fs';
import { UnknownOBTDevice } from './models/UnknownOBTDevice';
// import {WebUSB} from 'usb';
const usb = require('usb')
// import driveList from 'driveList';
const driveList = require('drivelist');
const deviceMap: Patient[] = _deviceMap.map((patient) => ({
    metaData: patient.metaData,
    data: patient.data.map((session) => ({
        ...session,
        gaps: session.gaps.map((gap) => ({
            start: new Date(gap.start), // Convert start to Date
            end: new Date(gap.end),   // Convert end to Date
        })),
        presses: session.presses.map((press) => ({
            timestamp: new Date(press.timestamp), // Convert timestamp to Date
            duration: press.duration,
        })),
        activities: session.activities.map((activity) => ({
            timestamp: new Date(activity.timestamp), // Convert timestamp to Date
            activity: activity.activity as ActivityTypes, // Ensure activity matches the type
        })),
    })),
}));
// Sources:
// https://www.electronforge.io/guides/framework-integration/react-with-typescript
// https://medium.com/@vamsikrishnaadusumalli999/creating-cross-platform-desktop-app-with-electron-js-and-react-to-understand-the-ipc-communication-518439877d9b
// https://electron-react-boilerplate.js.org/docs/native-modules/

// This allows TypeScript to pick up the magic constants that's auto-generated by Forge's Webpack
// plugin that tells the Electron app where to look for the Webpack-bundled app code (depending on
// whether you're running in development or production).
declare const MAIN_WINDOW_WEBPACK_ENTRY: string;
declare const MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY: string;

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
    app.quit();
}

let win: BrowserWindow = null;
const webusb = new usb.WebUSB({
    allowAllDevices: true
});

const createWindow = (): void => {
    // Create the browser window.  
    const mainWindow = new BrowserWindow({
        height: 600,
        width: 800,
        show: false,
        webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        },
    });
    win = mainWindow;
    mainWindow.maximize();
    mainWindow.show();
    // and load the index.html of the app.
    mainWindow.loadURL(MAIN_WINDOW_WEBPACK_ENTRY);
    // Open the DevTools.
    mainWindow.webContents.openDevTools();
    handleDeviceConnect();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    webusb.addEventListener('connect', handleDeviceConnect);
    // webusb.addEventListener('disconnect', handleDeviceDisconnect);
    createWindow();

    handleDeviceConnect();
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    webusb.removeEventListener('connect', broadcastAvailableDevices);
    webusb.removeEventListener('disconnect', broadcastAvailableDevices);
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.
ipcMain.on('send-message', (event, arg) => {
    //execute tasks on behalf of renderer process 
    console.log(arg) // prints "ping"
});

const getAvailableUSBDrives = (drives: Drive[], devices: UsbDevice[]): {patientData:PatientMetaData[],unknownDrives:{ deviceId: string; devicePath: string; fullPath: string; }[]} => {
    if(!drives || !devices || drives.length === 0 || devices.length === 0)
        return null;

    let usbDrives = drives.filter(drive => drive.isUSB);
    if (usbDrives.length === 0)
        return null;
    
    // Get OBT devices - these are both the id of a name in the these have a file called .OBT{id}
    let obtDevices = usbDrives.map(drive => {
        let mountpoint = drive.mountpoints[0];
        let dir = fs.readdirSync(mountpoint.path);
        console.log("Dir", dir);
        if(!dir || dir.length === 0)
            return null;
        
        let matchingDevice = devices.find(d => dir.some(o => path.parse(o).name == `.OBT${d.serialNumber}`));
        if(!matchingDevice)
            return null;

        return {
            deviceId: matchingDevice.serialNumber,
            devicePath: path.basename(mountpoint.path),
            fullPath: mountpoint.path
        }
    }).filter(o => o);
    console.log("OBT Devices",obtDevices);
    

    let mappedDevices: Patient[] = obtDevices.map(o => {
        let found = deviceMap.find(m => m.metaData.deviceId == o.deviceId);
        if(!found)
            return null;
        return found;
    }).filter(o => o);
    console.log("MappedDevices", mappedDevices);
    return {patientData: mappedDevices.map(o => o.metaData), unknownDrives: obtDevices.filter(o => !mappedDevices.some(d => d.metaData.deviceId == o.deviceId))}

    const circuitpyDrives = usbDrives;
    if(drives.length === 0 || usbDrives.length === 0 || circuitpyDrives.length === 0)
    return null;
    // return circuitpyDrives.map((drive:any) => {
    //     // const circuitpyMountPoint = drive.mountpoints.find((o:any) => o.label === 'CIRCUITPY');
    //     return {
    //     device: drive.device,
    //     description: drive.description,
    //     isUSB: drive.isUSB,
    //     label: drive.mountpoints.map((o: any) => o.label).join(', '),
    //     path: drive.mountpoints.map((o: any) => o.path).join(', '),
    //     };
    // });
}

const getAvailableUSBDevices = async (): Promise<UsbDevice[]> => {
    let usbDevices = await webusb.getDevices();
    console.log(usbDevices);
    console.log(usbDevices.map((o: any) => ({name:o.productName, descriptor: o.device.deviceDescriptor, portNumbers: o.device.portNumbers})));
    return usbDevices.map((device: any) => ({
        serialNumber: device.serialNumber,
        vendorId: device.vendorId,
        productId: device.productId
    }));
}

const handleDeviceConnect = async () => {
    let circuitpyDrives: Drive[] = [];
    let attempts = 60;
    for (let attempt = 0; attempt < attempts; attempt++) {
        let _circuitpyDrives = await driveList.list();
        if(_circuitpyDrives &&_circuitpyDrives.length > 0) {
            circuitpyDrives = _circuitpyDrives;
            break;
        }
        
        await new Promise(resolve => setTimeout(resolve, 500)); //Sleep 1 sec
    }
    let USBDevices = await getAvailableUSBDevices(); 
    console.log({circuitpyDrives, USBDevices});
    let usbDrives = getAvailableUSBDrives(circuitpyDrives, USBDevices);
    broadcastAvailableDevices(usbDrives);
}

// const handleDeviceDisconnect = async () => {
//     let circuitpyDrives = await getAvailableUSBDrives();
//     let USBDevices = await getAvailableUSBDevices(); 
//     broadcastAvailableDevices(circuitpyDrives, USBDevices);
// }



//https://github.com/node-usb/node-usb-example-electron/blob/main/main.js
const broadcastAvailableDevices = (usbDrives: { patientData: PatientMetaData[]; unknownDrives: UnknownOBTDevice[]; }) => {
    win.webContents.send('available-devices-broadcast', usbDrives);
};

// ipcMain.on('get-usb-devices-request', (event) => {
//     console.log("Received request")
//     getAvailableUSBDrives().then((data) => {
//         console.log("Got drives, ", data);
//         event.reply('get-usb-devices-response', data);
//     });
// });

ipcMain.on('available-devices-request', (event) => {
    handleDeviceConnect();
});

ipcMain.handle('create-device', async (e, device:UnknownOBTDevice, patientName: string) => {
    console.log("Create-device", e);
    let existingPatient = deviceMap.find(o => o.metaData.deviceId == device.deviceId);
    if(existingPatient) {
        existingPatient.metaData.devicePath = device.devicePath;
        existingPatient.metaData.patientName = patientName;
    } else {
        deviceMap.push({
            metaData: {
                deviceId: device.deviceId,
                devicePath: device.devicePath,
                patientName: patientName
            },
            data: []
        } as Patient);
    }

    let filePath = 'src/data/device_map.json';
    fs.readFile(filePath, 'utf8', function readFileCallback(err, data){
        if (err){
            console.log(err);
        } else {
        let json = JSON.stringify(deviceMap); //convert it back to json
        fs.writeFile(filePath, json, 'utf8', () => handleDeviceConnect()); // write it back 
    }});
    return;
});