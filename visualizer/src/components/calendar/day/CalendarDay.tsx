import React, { useEffect, useRef, useState } from 'react';
import { timeFloat } from '../helpers';
import mockdatapresses from '../../../mock_data_presses.json';
import * as Plot from "@observablehq/plot";
import { Button, ButtonGroup, Col, Container, Row } from 'react-bootstrap';
import { ChevronLeft, ChevronRight } from 'react-bootstrap-icons';


// https://observablehq.com/plot/getting-started
function CalendarDay({year, month, _date}:{year: number, month: number, _date: number}){
    console.log("CalendarDay");
    const [date, setDate] = useState(_date);
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
            x: (d) => d.timestamp.getDate(),
            fx: (d) => d.timestamp.getDate(),
            fill: "duration",
            title: (d) => d.timestamp.toISOString().split('T')[0],
            facet: "auto"
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
        <Col style={{display: 'flex', justifyContent: 'center'}}>
            <ButtonGroup style={{alignItems: 'center'}}>
                <Button className='btn btn-light' onClick={() => setDate(date - 1)}><ChevronLeft></ChevronLeft></Button>
                <div className='h3 bg-light' style={{marginBottom: 0}}>{new Date(year, month, date).toString()}</div>
                <Button className='btn btn-light' onClick={() => setDate(date + 1)}><ChevronRight></ChevronRight></Button>
            </ButtonGroup>
        </Col>
      </Row>
      <Row>
        <Col ref={columnRef}>
          <div ref={containerRef}/>
        </Col>
      </Row>
    </Container>
};
export default CalendarDay;