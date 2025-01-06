// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electron', {
    onDeviceUpdate: (callback: (data: string) => void) => {
        ipcRenderer.on('devices', (_, data) => callback(data));
    },
    getDeviceMapping: () => ipcRenderer.invoke('get-device-mapping'),
});