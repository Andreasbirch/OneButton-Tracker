import { UnknownDevice } from "../models/patients/PatientDevice";
import { PatientDevice } from "../models/patients/PatientDevice";

export type IDeviceService = {
    handleDeviceConnected: () => Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }>;
    handleDeviceDisconnected: () => Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }>;
}