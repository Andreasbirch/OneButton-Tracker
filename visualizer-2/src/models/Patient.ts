export type Gaps = {
    start: Date;
    end: Date;
};

export type Presses = {
    timestamp: Date;
    duration: Number;
}

export type ActivityTypes = "nonwear" | "still" | "moving" | "in vehicle";

export type Activity = {
    timestamp: Date;
    activity: ActivityTypes;
}

export type Session = {
    presses: Presses[];
    gaps: Gaps[];
    activities: Activity[];
}

export type PatientMetaData = {
    deviceId: String;
    devicePath: String;
    patientName: String;
}

export type Patient = {
    metaData: PatientMetaData;
    data: Session[];
};