import React, { useEffect, useRef, useState } from 'react';
import * as Plot from "@observablehq/plot";
import { Button, ButtonGroup, Col, Container, Row } from 'react-bootstrap';
import { ChevronLeft, ChevronRight } from 'react-bootstrap-icons';
import { GetGapIntersectForDate } from '../helpers';
import { Gaps, Press, Session } from '../../../models/patients/PatientData';

type CalendarDayProps = {
  year: number, 
  month: number, 
  _date: number, 
  width: number
  sessions: Session[];
}

// https://observablehq.com/plot/getting-started
function CalendarDay({year, month, _date, width, sessions}:CalendarDayProps){
    const [date, setDate] = useState(_date);
    const containerRef = useRef<any>(null);
    const [data, setData] = useState<Press[]>([]);
    const [nonWearData, setNonWearData] = useState<Gaps[]>([]);

    useEffect(() => {
        setDate(_date);
    }, [_date]);

    useEffect(() => {
        let targetDate = new Date(year, month, date);
        let dataGaps = sessions.flatMap(o => o.gaps);
        let presses = sessions.flatMap(o => o.presses);
        console.log(dataGaps, presses);
        let _nonWearData = GetGapIntersectForDate(dataGaps.map(o => ({start: new Date(o.start), end: new Date(o.end)})), targetDate);
        console.log(_nonWearData);
        let _data = presses
            .filter(o => o.timestamp.getFullYear() === year)
            .filter(o => o.timestamp.getMonth() === month)
            .filter(o => o.timestamp.getDate() === date);
        if (_data.length === 0) return; // Avoid processing empty data

        let tempFirstDate: Date = _data[0].timestamp;
        let firstDate = new Date(Date.UTC(tempFirstDate.getFullYear(), tempFirstDate.getMonth(), tempFirstDate.getDate(), 0, 0, 0));
        let emptyFirst = { timestamp: firstDate, duration: 0 };

        let lastDate = new Date(Date.UTC(tempFirstDate.getFullYear(), tempFirstDate.getMonth(), tempFirstDate.getDate(), 23, 59, 59));
        let emptyLast:Press = { timestamp: lastDate, duration: 0 };

        setData([emptyFirst, ..._data, emptyLast]); // Update state with new data
        setNonWearData(_nonWearData);
    }, [year, month, date]);

    useEffect(() => {
      if (data === undefined) return;
      containerRef.current.innerHTML = ''; // Clear previous plot

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
          Plot.barX(nonWearData, {
            x1: 'start',
            x2: 'end',
            fill: 'lightgray'
          })
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
                <div className='h3 bg-light' style={{marginBottom: 0}}>{new Date(year, month, date).toLocaleDateString('en-GB')}</div>
                <Button className='btn btn-light' onClick={() => setDate(date + 1)}><ChevronRight></ChevronRight></Button>
            </ButtonGroup>
        </Col>
      </Row>
      <Row>
        <Col>
          <div ref={containerRef}/>
        </Col>
      </Row>
    </Container>
};
export default CalendarDay;