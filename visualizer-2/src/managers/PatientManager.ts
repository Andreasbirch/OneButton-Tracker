import { PatientData, PatientDataMap, Presses, Session } from "../models/patients/PatientData";
import { IPatientDataManager, IPatientDeviceManager } from "./IPatientManager";
import { PatientDevice, PatientDeviceMap } from "../models/patients/PatientDevice";

import patient_device_map from '../data/patient_devices.json';
import patient_data_map from '../data/patient_data.json';

const patientDeviceMap: PatientDeviceMap = patient_device_map as PatientDeviceMap;

const convertToMap = (data: any): PatientDataMap => {
    const result: PatientDataMap = {};

    Object.keys(data).forEach((id) => {
        const patientData = data[id];
        
        const convertedSessions = patientData.sessions.map((session: any): Session => {
            const convertedGaps = session.gaps.map((gap: any) => ({
                start: new Date(gap.start),
                end: new Date(gap.end),
            }));

            const convertedPresses = session.presses.map((press: any): Presses => ({
                timestamp: new Date(press.timestamp),
                duration: press.duration,
            }));

            return {
                gaps: convertedGaps,
                presses: convertedPresses,
                activities: session.activities,
            };
        });

        result[id] = {
            id: patientData.id,
            sessions: convertedSessions,
        };
    });

    return result;
};
const patientDataMap: PatientDataMap = convertToMap(patient_data_map);



class PatientManager implements IPatientDeviceManager, IPatientDataManager {
    // Patient Device Manager
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
            throw new Error("Patient device not found for id " + patientDevice.id);
        }
    };




    // Patient data manager
    getPatientDataMap = () => {
        return patientDataMap;
    };
    getPatientData = (id: string) => {
        return patientDataMap[id];
    };
    addPatientData = (patientData: PatientData) => {
        if(patientDataMap[patientData.id]) {
            throw new Error("Patient already exists");
        } else {
            patientDataMap[patientData.id] = patientData;
        }
    };
    updatePatientData = (patientData: PatientData) => {
        if(patientDataMap[patientData.id]) {
            patientDataMap[patientData.id] = patientData;
        } else {
            throw new Error("Patient data not found for id " + patientData.id);
        }

    }
    addPatientSession = (id: string, session: Session) => {
        if(!patientDataMap[id].sessions) {
            patientDataMap[id].sessions = [session];   
        } else {
            patientDataMap[id].sessions.push(session);
        }
    }
}