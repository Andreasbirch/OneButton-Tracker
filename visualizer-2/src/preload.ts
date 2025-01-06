import { ipcRenderer } from "electron";

// See the Electron documentation for details on how to use preload scripts:
ipcRenderer.send('send-message', "Hej");
