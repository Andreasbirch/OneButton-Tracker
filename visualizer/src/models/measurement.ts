export interface IMeasurement {
    timestamp: Date,
    activityClassification: IActivityClassification,
    stabilityClassification: stabilityClassification,
    shakeDetection: boolean,
    stepCount: number,
    qX: number,
    qY: number,
    qZ: number,
    qW: number,
    accX: number,
    accY: number,
    accZ: number,
    tiltUpwards: boolean,
    tiltForwards: boolean,
    vbat: number,
    vusb: number
}

export type stabilityClassification = 'onTable' | 'inMotion' | 'stable';

export interface IActivityClassification {
    running: number,
    tilting: number,
    onFoot: number,
    inVehicle: number,
    still: number,
    walking: number,
    onBicycle: number,
    onStaits: number,
    mostLikely: string
}