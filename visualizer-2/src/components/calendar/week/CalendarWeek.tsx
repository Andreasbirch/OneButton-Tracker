import React, { useEffect, useRef, useState } from 'react';
import { GetGapIntersectForDate, getWeek, timeFloat } from '../helpers';
import * as Plot from "@observablehq/plot";
import { Button, ButtonGroup, Col, Container, Row } from 'react-bootstrap';
import { ChevronLeft, ChevronRight } from 'react-bootstrap-icons';
import { Gaps, Session } from '../../../models/patients/PatientData';

type CalendarWeekProps = {
  year: number,
  _week: number,
  width: number
  sessions: Session[];
}

function CalendarWeek({year, _week, width, sessions}: CalendarWeekProps) {
  const [week, setWeek] = useState(_week);
  
    let _data = sessions.flatMap(o => o.presses)
      .filter(o => o.timestamp.getFullYear() == year)
      .filter(o => getWeek(o.timestamp) == week);
    let activity = sessions.flatMap(o => o.activities)
    let dataGaps = sessions.flatMap(o => o.gaps);
    
    let activitySpans = sessions.flatMap(o => o.activitiesSpan)
      .filter(o => new Date(o.start).getFullYear() == year)
      .filter(o => getWeek(new Date(o.start)) == week);

    // let _nonWearData = GetGapIntersectForDate<Gaps>(dataGaps, targetDate);
    
    const containerRef = useRef<any>(null);
    const [data, setData] = useState(_data);
    useEffect(() => {
      if (data === undefined) return;
      const plot = Plot.plot({
        width: width,
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
          Plot.barY([...Array(7).keys()].map((o,i) => ({y1: 0, y2: 24, x: i})),{
            y1: 0,
            y2: 23.99,
            fill: 'lightgray',
            x: 'x',
          }),
          Plot.barY(activitySpans.filter(o => o.activity !== 'still'), {
            y1: (d) => timeFloat(d.start),
            y2: (d) => timeFloat(d.end),
            x: (d) => new Date(d.start).getUTCDay(),
            fill: 'lightblue',
            fx: (d) => getWeek(d.start)
          }),
          Plot.barY(activitySpans.filter(o => o.activity === 'still'), {
            y1: (d) => timeFloat(d.start),
            y2: (d) => timeFloat(d.end),
            x: (d) => new Date(d.start).getUTCDay(),
            fill: 'lightgreen',
            fx: (d) => getWeek(d.start)
          }),
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
          Plot.frame(),
        ]
      });
      containerRef.current.append(plot);
        
      return () => plot.remove();
    }, [data, week]); // Run on data change

        //return data.filter(o => o.date.getDay() == 4)

    return <Container>
      {/* <Row>
        <Col style={{display: 'flex', justifyContent: 'center'}}>
            <ButtonGroup style={{alignItems: 'center'}}>
                <Button className='btn btn-light' onClick={() => setWeek(week - 1)}><ChevronLeft></ChevronLeft></Button>
                <div className='h3 bg-light' style={{marginBottom: 0}}>Week {week}</div>
                <Button className='btn btn-light' onClick={() => setWeek(week + 1)}><ChevronRight></ChevronRight></Button>
            </ButtonGroup>
        </Col>
      </Row> */}
      <Row>
        <Col>
          <div ref={containerRef}/>
        </Col>
      </Row>
    </Container>
}

export default CalendarWeek;