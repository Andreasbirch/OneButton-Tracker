import { UnknownDevice } from "../models/patients/PatientDevice";
import { PatientDevice } from "../models/patients/PatientDevice";

export type IDeviceManager = {
    handleDeviceConnected: () => Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }>;
    handleDeviceDisconnected: () => Promise<{ patientDevices: PatientDevice[]; unknownDevices: UnknownDevice[]; }>;
}