import React, { ChangeEventHandler } from "react"
import { useState } from "react";
import Papa from "papaparse"

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

    var header = [
        "Timestamp", 
        "activity_running", 
        "activity_unknown", 
        "activity_tilting", 
        "activity_on_foot", 
        "activity_in_vehicle", 
        "activity_still", 
        "activity_walking", 
        "activity_most_likely", 
        "stability_classification", 
    ];

    const parseCSV = (file: File) => {
        const reader = new FileReader();
        reader.onload = () => {
            const csvData = reader.result;

            Papa.parse(csvData, {
                header: ["Timestamp", "activity_running", "activity_unknown", "activity_tilting", "activity_on_foot", "activity_in_vehicle", "activity_still", "activity_walking", "activity_most_likely", "stability_classification", ],
                skipEmptyLines: true,
                
                complete: (result) => {
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
            <pre>{JSON.stringify(fileJson, null, 2)}</pre>
        </label>
    </div>
};

export default FileUpload;