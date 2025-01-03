import React, { useEffect, useRef, useState } from 'react';
import { groupBy, getWeek, timeFloat } from '../helpers';
import mockdatapresses from '../../../mock_data_presses.json';
import * as Plot from "@observablehq/plot";
import { Col, Container, Row } from 'react-bootstrap';

function CalendarWeek({year, week}: {year: number, week: number}) {
    let _data = mockdatapresses.map(o => ({timestamp: new Date(o.timestamp), duration: o.duration}))
    .filter(o => o.timestamp.getFullYear() == year)
    .filter(o => getWeek(o.timestamp) == week);
    
    const columnRef = useRef<HTMLDivElement>(null);
    const [plotWidth, setPlotWidth] = useState<number>(0);
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
        x: {
          // padding: 0,
          tickFormat: Plot.formatWeekday("dk", "short"),
          tickSize: 0,
          domain: [1, 2, 3, 4, 5, 6, 0],
          axis: "top"
        },
        y: {
          domain: [24, 0],
          tickSize: 0,
          grid: true
        },
        color: {
          scheme: "Oranges",
          type: "diverging"
        },
        marks: [
          Plot.barY(data, {
            // lay the days out in the x direction based on the week of the year
            y1: (d) => timeFloat(d.timestamp),
            y2: (d) => timeFloat(new Date(d.timestamp.getTime() + d.duration * 500)),
            // lay the days out in the x direction based on day of the week
            x: (d) => d.timestamp.getUTCDay(),
            fill: "duration",
            title: (d) => d.timestamp,
            fx: (d) => getWeek(d.timestamp),
          }),
          // Plot.barY(timechunk_data.filter(o => o.start.getFullYear() == 2024 && o.start.getMonth() == 3 && o.start.getWeek() == 16), {
          //   // lay the days out in the x direction based on the week of the year
          //   y1: (d) => d.start.toTimeFloat(),
          //   y2: (d) => d.end.toTimeFloat(),
          //   // lay the days out in the x direction based on day of the week
          //   x: (d) => d.start.getUTCDay(),
          //   fx: (d) => d.start.getWeek(),
          //   fill: (d) => "lightgray",
          // }),
          Plot.axisFx({
            dy: -14,
            text: "",
            label: `Week ${getWeek(data[0].timestamp)}`
            //tickFormat: Plot.formatMonth("dk", "long")
          }),
          Plot.frame(),
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
}

export default CalendarWeek;