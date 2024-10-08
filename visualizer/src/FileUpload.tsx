import React, { ChangeEventHandler } from "react"
import { useState } from "react";
import Papa from "papaparse";
import Charts from "./Charts";
import { IMeasurement } from "./models/measurement";

const FileUpload = () => {
    const [fileJson, setFileJson] = useState(null);

    const handleFileUpload = (e: any) => {
        console.log(typeof(e));
        const file = e.target.files[0];
        if (file && file.type === "text/csv") 
            parseCSV(file);
        else {
            alert("Den indsatte fil kunne ikke indlæses");
        }
    };

    var headers = [
        "Timestamp", 
        "activity_classification", 
        "stability_classification", 
        "shake_detection",
        "step_count",
        "q_x",
        "q_y",
        "q_z",
        "q_w",
        "acc_x",
        "acc_y",
        "acc_z",
        "tilt_up",
        "tilt_forward",
        "vbat_voltage",
        "usb_voltage"
    ];

    const parseCSV = (file: File) => {
        const reader = new FileReader();
        reader.onload = () => {
            let csvData:any = headers.join(";") + "\n" + reader.result;

            Papa.parse(csvData, {
                header: true,
                skipEmptyLines: true,
                delimiter: ";",
                dynamicTyping: true,
                complete: (result:any) => {
                    setFileJson(result.data);
                },
                error: (error) => {
                    console.error("Error parsing CSV: ", error);
                },
            });
        };
        reader.readAsText(file);
    };

    return <div>
        <label>
            Upload din fil her
            <input type="file" accept=".csv" onChange={handleFileUpload} />
            {fileJson && <Charts measurements={fileJson} />}
            
        </label>
    </div>
};

export default FileUpload;