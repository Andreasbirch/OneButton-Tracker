import React, { useEffect, useRef, useState } from 'react';
import { groupBy, getWeek, timeFloat } from '../helpers';
import mockdatapresses from '../../../mock_data_presses.json';
import * as Plot from "@observablehq/plot";
import { Col, Container, Row } from 'react-bootstrap';

// https://observablehq.com/plot/getting-started
function CalendarDay({year, month, date}:{year: number, month: number, date: number}){
    let _data = mockdatapresses.map(o => ({timestamp: new Date(o.timestamp), duration: o.duration}))
        .filter(o => o.timestamp.getFullYear() == year)
        .filter(o => o.timestamp.getMonth() == month)
        .filter(o => o.timestamp.getDate() == date);

    const columnRef = useRef<HTMLDivElement>(null);
    const [plotWidth, setPlotWidth] = useState<number>(1000);
    useEffect(() => {
      const updateWidth = () => {
        if (columnRef.current) {
          setPlotWidth(columnRef.current.getBoundingClientRect().width);
        }
      };
      
      // Initial width calculation
      updateWidth();

      // Update width on window resize
      window.addEventListener('resize', updateWidth);
      return () => window.removeEventListener('resize', updateWidth);
    }, []); // Run on mount
    
    const containerRef = useRef<any>(null);
    const [data, setData] = useState(_data);
    useEffect(() => {
      if (data === undefined) return;
      const plot = Plot.plot({
        width: plotWidth,
        aspectRatio: 10,
        y: {
          domain: [24, 0],
          tickSize: 0,
          grid: true
        },
        color: {
          scheme: "Oranges"
        },
        marks: [
          Plot.barY(data, {
            // lay the days out in the x direction based on the week of the year
            y1: (d) => timeFloat(d.timestamp),
            y2: (d) => timeFloat(new Date(d.timestamp.getTime() + d.duration * 1000)),
            // lay the days out in the x direction based on day of the week
            x: (d) => d.timestamp.getUTCDay(),
            fx: (d) => d.timestamp.getUTCDay(),
            fill: "duration",
            title: (d) => d.timestamp.toISOString().split('T')[0],
          }),
          Plot.axisFx({
            dy: -14,
            text: "",
            label: `${data[0].timestamp.toISOString().split('T')[0]}`
            //tickFormat: Plot.formatMonth("dk", "long")
          }),
        ]
      });
      containerRef.current.append(plot);
        
      return () => plot.remove();
    }, [data]); // Run on data change

        //return data.filter(o => o.date.getDay() == 4)

    return <Container>
      <Row>
        <Col ref={columnRef}>
          <div ref={containerRef}/>
        </Col>
      </Row>
    </Container>
};
export default CalendarDay;