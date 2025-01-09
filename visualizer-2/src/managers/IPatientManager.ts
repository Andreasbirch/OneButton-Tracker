import { PatientDevice, PatientDeviceMap } from '../models/patients/PatientDevice';
import { PatientData, Session } from '../models/patients/PatientData';

export type IPatientDeviceManager = {
  getPatientDeviceMap: () => PatientDeviceMap;
  getPatientDevice: (id: string) => PatientDevice;
  addPatientDevice: (patientDevice: PatientDevice) => void;
  updatePatientDevice: (patientDevice: PatientDevice) => void;
}

export type IPatientDataManager = {
  getPatientDatas: () => PatientData[];
  getPatientData: (id: string) => PatientData;
  addPatientData: (patientData: PatientData) => void;
  addPatientSession: (id:string, session: Session) => void;
}