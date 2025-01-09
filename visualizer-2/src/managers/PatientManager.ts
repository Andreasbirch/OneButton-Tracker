import { PatientData, Session } from "../models/patients/PatientData";
import { IPatientDataManager, IPatientDeviceManager } from "./IPatientManager";
import { PatientDevice, PatientDeviceMap } from "../models/patients/PatientDevice";

import patient_device_map from '../data/patient_devices.json';

const patientDeviceMap: PatientDeviceMap = patient_device_map as PatientDeviceMap

class PatientManager implements IPatientDeviceManager {
    getPatientDeviceMap = (): PatientDeviceMap => {
        return patientDeviceMap;
    };

    getPatientDevice = (id: string): PatientDevice => {
        return patientDeviceMap[id];
    };

    addPatientDevice = (patientDevice: PatientDevice): void => {
        if (patientDeviceMap[patientDevice.id])
            throw new Error("Patient already exists");
        patientDeviceMap[patientDevice.id] = patientDevice;
    };

    updatePatientDevice = (patientDevice: PatientDevice): void => {
        if (patientDeviceMap[patientDevice.id]) {
            patientDeviceMap[patientDevice.id] = patientDevice;
        } else {
            throw new Error("Patient device not found for update");
        }
    };
}