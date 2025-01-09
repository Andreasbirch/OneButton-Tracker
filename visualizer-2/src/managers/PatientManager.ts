import { PatientData, PatientDataMap, Presses, Session } from "../models/patients/PatientData";
import { IPatientDataManager, IPatientDeviceManager } from "./IPatientManager";
import { PatientDevice, PatientDeviceMap } from "../models/patients/PatientDevice";

import fs from 'fs';
const patientDevicesPath = "src/data/patient_devices.json";
const patientDataPath = "src/data/patient_data.json";

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

class PatientManager implements IPatientDeviceManager, IPatientDataManager {
    // Patient Device Manager
    getPatientDeviceMap = (): PatientDeviceMap => {
        var patientDeviceMap = JSON.parse(fs.readFileSync(patientDevicesPath, 'utf8')) as PatientDeviceMap;
        return patientDeviceMap;
    };

    getPatientDevice = (id: string): PatientDevice => {
        return this.getPatientDeviceMap()[id];
    };

    addPatientDevice = (patientDevice: PatientDevice): void => {
        var patientDeviceMap = this.getPatientDeviceMap();
        if (patientDeviceMap[patientDevice.id])
            throw new Error("Patient already exists");

        patientDeviceMap[patientDevice.id] = patientDevice;
        fs.writeFileSync(patientDevicesPath, JSON.stringify(patientDeviceMap, null, 4));
    };

    updatePatientDevice = (patientDevice: PatientDevice): void => {
        var patientDeviceMap = this.getPatientDeviceMap();
        if (patientDeviceMap[patientDevice.id]) {
            patientDeviceMap[patientDevice.id] = patientDevice;
            fs.writeFileSync(patientDevicesPath, JSON.stringify(patientDeviceMap, null, 4));
        } else {
            throw new Error("Patient device not found for id " + patientDevice.id);
        }
    };




    // Patient data manager
    getPatientDataMap = () => {
        var patientDataMap = convertToMap(JSON.parse(fs.readFileSync(patientDataPath, 'utf8')));
        return patientDataMap;
    };
    getPatientData = (id: string) => {
        var patientDataMap = this.getPatientDataMap();
        return patientDataMap[id];
    };
    addPatientData = (patientData: PatientData) => {
        var patientDataMap = this.getPatientDataMap();
        if(patientDataMap[patientData.id]) {
            throw new Error("Patient already exists");
        } else {
            patientDataMap[patientData.id] = patientData;
            fs.writeFileSync(patientDataPath, JSON.stringify(patientDataMap, null, 4));
        }
    };
    updatePatientData = (patientData: PatientData) => {
        var patientDataMap = this.getPatientDataMap();
        if(patientDataMap[patientData.id]) {
            patientDataMap[patientData.id] = patientData;
            fs.writeFileSync(patientDataPath, JSON.stringify(patientDataMap, null, 4));
        } else {
            throw new Error("Patient data not found for id " + patientData.id);
        }
    }
    addPatientSession = (id: string, session: Session) => {
        var patientDataMap = this.getPatientDataMap();
        if(!patientDataMap[id].sessions) {
            patientDataMap[id].sessions = [session];   
        } else {
            patientDataMap[id].sessions.push(session);
        }
        fs.writeFileSync(patientDataPath, JSON.stringify(patientDataMap, null, 4));
    }
}

export {PatientManager};