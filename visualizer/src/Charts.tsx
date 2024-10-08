import { Chart, plugins } from "chart.js/auto";
import { IMeasurement } from "./models/measurement";

const Charts = (measurements: any) => {
    let m: IMeasurement[] = measurements.measurements;
    console.log("I received measurements", m.length, m);
    console.log(m[0]);
    // const battery_data: any[] = measurements.map((e: IMeasurement) => {
    //     e.timestamp, 
    //     e.vbat,
    //     e.vusb
    // });

    const config = {
        type: 'line',
        // data: battery_data,
        options: {

        },
        plugins: []
    }
    return <div>
        <p>Charts</p>
    </div>
};

export default Charts;