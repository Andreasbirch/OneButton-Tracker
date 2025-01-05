import React, { useEffect, useRef, useState } from 'react';
import { groupBy, getWeek, timeFloat } from '../helpers';
import mockdatapresses from '../../../mock_data_presses.json';
import * as Plot from "@observablehq/plot";
import { Col, Container, Row } from 'react-bootstrap';

// https://observablehq.com/plot/getting-started
function CalendarDay({year, month, date, width}:{year: number, month: number, date: number, width: number}){
    let _data = mockdatapresses.map(o => ({timestamp: new Date(o.timestamp), duration: o.duration}))
        .filter(o => o.timestamp.getFullYear() == year)
        .filter(o => o.timestamp.getMonth() == month)
        .filter(o => o.timestamp.getDate() == date);
    let _date: Date = _data[0].timestamp;
    let firstDate = new Date(Date.UTC(_date.getFullYear(), _date.getMonth(), _date.getDate(), 0, 0, 0));
    let emptyFirst = {
        timestamp: firstDate,
        duration: 0,
    }
    
    let lastDate = new Date(Date.UTC(_date.getFullYear(), _date.getMonth(), _date.getDate(), 23, 59, 59));
    let emptyLast = {
        timestamp: lastDate,
        duration: 0,
    }
    
    _data = [emptyFirst, ..._data, emptyLast];


    const containerRef = useRef<any>(null);
    const [data, setData] = useState(_data);
    useEffect(() => {
      if (data === undefined) return;
      const plot = Plot.plot({
        width,
        y: {
          grid: true
        },
        x: {
          ticks: 'hour',
          grid: true
        },
        color: {
          scheme: "Oranges"
        },
        marks: [
          Plot.ruleX(data, {
            x: (d) => d.timestamp,
            stroke: "duration",
            strokeWidth: 4,
            // lay the days out in the x direction based on day of the week
            fill: "duration",
            title: (d) => d.timestamp,
            y: (d) => d.duration / 1000
          }),
        ]
      });
      containerRef.current.append(plot);
        
      return () => plot.remove();
    }, [data]); // Run on data change

        //return data.filter(o => o.date.getDay() == 4)

    return <Container>
      <Row>
        <Col>
          <div ref={containerRef}/>
        </Col>
      </Row>
    </Container>
};
export default CalendarDay;