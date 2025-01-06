import { ipcRenderer } from "electron";

// See the Electron documentation for details on how to use preload scripts:
console.log("Bare fra preload");
ipcRenderer.send('send-questions', "Hej");
