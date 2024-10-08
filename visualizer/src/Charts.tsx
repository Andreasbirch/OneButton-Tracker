import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, TimeScale } from 'chart.js';
import { IMeasurement } from "./models/measurement";
import parseMeasurement from "./models/parsers/measurementParser";
import { Line } from "react-chartjs-2";
import zoomPlugin from 'chartjs-plugin-zoom';
import 'chartjs-adapter-date-fns';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    TimeScale,
    Title,
    Tooltip,
    Legend,
    zoomPlugin
  );

const Charts = (data: any) => {

    // const measurements = data.data.map((e:any) => parseMeasurement(e));
    const measurements = data.data.map((e:any) => parseMeasurement(e));
    

    const battery_data: {timestamp: Date, vbat: number, vusb: number}[] = measurements.map((e: IMeasurement) => {
        return {
            timestamp: e.timestamp, 
            vbat: e.vbat,
            vusb: e.vusb
        }
    });
    
    console.log(battery_data);

    const chartData = {
        labels: battery_data.map(e => e.timestamp),
        datasets: [
            {
                label: 'vbat',
                data: battery_data.map(e => e.vbat)
            },
            {
                label: 'vusb',
                data: battery_data.map(e => e.vusb)
            }
        ] 
    }

    const options= {
        plugins: {
          title: {
            text: 'Chart.js Time Scale',
            display: true
          },
          zoom: {
            zoom: {
                wheel: {
                    enabled: true,
                    modifierKey: 'shift' as const
                },
                pinch: {
                    enabled: true
                },
                mode: 'xy' as const,
            },
            pan: {
                enabled: true,
                mode: 'xy' as const,
                scalemode: 'xy' as const
            }
          },
        },
        scales: {
          x: {
            type: "time" as const,
          },
          y: {
            title: {
              display: true,
              text: 'value'
            }
          }
        },
      };

    // const options = {
    //     responsive: true,
    //     plugins: {
    //         legend: {
    //             position: 'top' as const,
    //         },
    //         title: {
    //             display: true,
    //             text: 'Battery degradation',
    //         },
    //     },
    //     scales: {
    //         x: {
    //             type: 'timeseries',
    //             time: {
    //                 unit: 'minute',
    //                 tooltipFormat: 'HH mm ss',
    //             },
    //             title: {
    //                 display: true,
    //                 text: 'Date'
    //             }
    //         },
    //         y: {
    //             beginAtZero: true, // Start the y-axis at 0
    //             title: {
    //                 display:true,
    //                 text: 'Voltage'
    //             }
    //         },
    //     },
    // }

    return <div>
        <p>Charts</p>
        <Line data={chartData} options={options}></Line>
    </div>
};

export default Charts;