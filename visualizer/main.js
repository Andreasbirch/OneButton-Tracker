// Modules to control application life and create native browser window
const { app, BrowserWindow } = require('electron');
const path = require('path');
const usb = require('usb');
const fs = require('fs');
const driveList = require('drivelist');

let windows = [];

const webusb = new usb.WebUSB({
    allowAllDevices: true
});

const getCircuitpyDrives = async () => {
  const drives = await driveList.list();
  
  if (!drives || drives.length === 0) {
    console.log("No devices found");
  } else {
    const usbDrives = drives.filter(drive => drive.isUSB);
    if (usbDrives.length > 0) {
      const circuitpyDrives = usbDrives.filter(drive =>
        drive.mountpoints.some(o => o.label === 'CIRCUITPY')
      );
      if (circuitpyDrives.length > 0) {
        const circuitpyMountPoints = circuitpyDrives.map(drive => {
          const circuitpyMountPoint = drive.mountpoints.find(o => o.label === 'CIRCUITPY');
          return `${circuitpyMountPoint.label} ${circuitpyMountPoint.path}`;
        });
        return circuitpyMountPoints;
      }
    }
  }
  return null;
}


const getDeviceMapping = async () => {
  let usbDevices = await webusb.getDevices();
  let drives = await driveList.list();

  let deviceInfo = usbDevices;
  // let deviceInfo = usbDevices.map(device => ({
  //   serialNumber: device.serialNumber,
  //   vendorId: device.vendorId,
  //   productId: device.productId,
  // }));

  let driveInfo = drives.map(drive => ({
    device: drive.device,
    description: drive.description,
    isUSB: drive.isUSB,
  }));

  console.log('USB Devices:', deviceInfo);
  console.log('Drives:', driveInfo);

  return { deviceInfo, driveInfo };
}



const handleDeviceConnect = async () => {
  let data = "No devices found";
  let attempts = 60;
  for (let attempt = 0; attempt < attempts; attempt++) {
    let circuitpyDrives = await getCircuitpyDrives();
    if(circuitpyDrives) {
      data = circuitpyDrives.join('\n');
      break;
    }
    
    await new Promise(resolve => setTimeout(resolve, 500)); //Sleep 1 sec
  }
  
  showDevices(data);
}

const handleDeviceDisconnect = async () => {
  let data = "No devices found";
  let circuitpyDrives = await getCircuitpyDrives();
  if(circuitpyDrives)
    data = circuitpyDrives.join('\n');
  
  showDevices(data);
}

//https://github.com/node-usb/node-usb-example-electron/blob/main/main.js
const showDevices = (data) => {
    windows.forEach(win => {
        if (win) {
            win.webContents.send('devices', data);
        }
    });
};

const createWindow = () => {
    // Create the browser window.
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });

    // and load the index.html of the app.
    win.loadFile('public/index.html');

    // Open the DevTools.
    // win.webContents.openDevTools()

    windows.push(win);
    handleDeviceConnect();
    getDeviceMapping();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    webusb.addEventListener('connect', handleDeviceConnect);
    webusb.addEventListener('disconnect', handleDeviceDisconnect);

    createWindow();

    app.on('activate', () => {
        // On macOS it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    webusb.removeEventListener('connect', showDevices);
    webusb.removeEventListener('disconnect', showDevices);

    app.quit();
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.