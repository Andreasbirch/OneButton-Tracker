export type Gaps = {
    start: Date;
    end: Date;
};

export type Press = {
    timestamp: Date;
    duration: number;
}

export type ActivityTypes = "nonwear" | "still" | "moving" | "in vehicle";

export type Activity = {
    timestamp: Date;
    activity: ActivityTypes;
}

export type ActivitySpan = {
    start: Date;
    end: Date;
    activity: ActivityTypes;
}

export type Session = {
    id: number;
    presses: Press[];
    gaps: Gaps[];
    activities: Activity[];
    activitiesSpan: ActivitySpan[];
}

export type PatientData = {
    id: string;
    sessions: Session[];
};

export type PatientDataMap = {
    [id: string]: PatientData;
}