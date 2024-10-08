import { IMeasurement, stabilityClassification } from "../measurement";
// Parsing function to convert JSON objects into IMeasurement
function parseMeasurement(data: any): IMeasurement {
    const activityClassification = JSON.parse(data.activity_classification.replace(/'/g, '"'));

    // Stability classification conversion
    let stability: stabilityClassification;
    switch (data.stability_classification.toLowerCase()) {
        case 'on table':
            stability = 'onTable';
            break;
        case 'in motion':
            stability = 'inMotion';
            break;
        case 'still':
            stability = 'still';
            break;
        default:
            throw new Error(`Unknown stability classification: ${data.stability_classification}`);
    }

    // Create IMeasurement object
    const measurement: IMeasurement = {
        timestamp: new Date(data.Timestamp),
        activityClassification: {
            running: activityClassification.Running,
            tilting: activityClassification.Tilting,
            onFoot: activityClassification['On-Foot'],
            inVehicle: activityClassification['In-Vehicle'],
            still: activityClassification.Still,
            walking: activityClassification.Walking,
            onBicycle: activityClassification['On-Bicycle'],
            onStaits: activityClassification['OnStairs'],
            mostLikely: activityClassification.most_likely
        },
        stabilityClassification: stability,
        shakeDetection: data.shake_detection === 'True',
        stepCount: data.step_count,
        qX: data.q_x,
        qY: data.q_y,
        qZ: data.q_z,
        qW: data.q_w,
        accX: data.acc_x,
        accY: data.acc_y,
        accZ: data.acc_z,
        tiltUpwards: data.tilt_up === 'True',
        tiltForwards: data.tilt_forward === 'False',
        vbat: data.vbat_voltage,
        vusb: data.usb_voltage
    };

    return measurement;
}
