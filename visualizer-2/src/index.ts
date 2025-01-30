import { app, BrowserWindow, ipcMain } from 'electron';
import { PatientRepository } from './managers/PatientRepository';
import { DeviceService } from './managers/DeviceService';
import { UnknownDevice } from './models/patients/PatientDevice';
const usb = require('usb')

// Sources:
// https://www.electronforge.io/guides/framework-integration/react-with-typescript
// https://medium.com/@vamsikrishnaadusumalli999/creating-cross-platform-desktop-app-with-electron-js-and-react-to-understand-the-ipc-communication-518439877d9b
// https://electron-react-boilerplate.js.org/docs/native-modules/

// This allows TypeScript to pick up the magic constants that's auto-generated by Forge's Webpack
// plugin that tells the Electron app where to look for the Webpack-bundled app code (depending on
// whether you're running in development or production).
declare const MAIN_WINDOW_WEBPACK_ENTRY: string;

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
    app.quit();
}

const patientManager: PatientRepository = new PatientRepository();
const deviceManager: DeviceService = new DeviceService();
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
    handleDeviceConnected();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    webusb.addEventListener('connect', handleDeviceConnected);
    webusb.addEventListener('disconnect', handleDeviceDisconnected);
    createWindow();

    handleDeviceConnected();
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    webusb.removeEventListener('connect', handleDeviceConnected);
    webusb.removeEventListener('disconnect', handleDeviceConnected);
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

const handleDeviceConnected = async () => {
    console.log("HandleDeviceConnected");
    let availableDevices = await deviceManager.getAvailableDevices();
    win.webContents.send('available-devices-broadcast', availableDevices);
}

const handleDeviceDisconnected = async () => {
    console.log("HandleDeviceDisconnected");
    let availableDevices = await deviceManager.getAvailableDevices();
    win.webContents.send('available-devices-broadcast', availableDevices);
}

ipcMain.on('available-devices-request', (event) => {
    handleDeviceConnected();
});

ipcMain.handle('create-device', async (e, device:UnknownDevice, patientName: string) => {
    if(patientManager.getPatientDevice(device.id))
        return;
    
    patientManager.addPatientDevice({
        id: device.id,
        devicePath: device.devicePath,
        patientName: patientName
    });
    
    handleDeviceConnected();
    return;
});