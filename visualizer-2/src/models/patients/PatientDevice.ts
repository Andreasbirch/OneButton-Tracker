export type PatientDevice = {
    id: string;
    devicePath: string;
    patientName: string;
}

export type PatientDeviceMap = {
    [id: string]: PatientDevice;
}

export type UnknownDevice = {
    id: string;
    devicePath: string;
}