import React, { useEffect, useRef, useState } from 'react';
import { GetGapIntersectForDate, getWeek, timeFloat } from '../helpers';
import * as Plot from "@observablehq/plot";
import { Button, Col, Container, Row } from 'react-bootstrap';
import { SquareFill } from 'react-bootstrap-icons';
import { ActivitySpan, Gaps, Session } from '../../../models/patients/PatientData';

type CalendarWeekProps = {
  year: number,
  _week: number,
  width: number
  sessions: Session[];
  onMonthClick: (month: number) => void;
}

function CalendarWeek({year, _week, width, sessions, onMonthClick}: CalendarWeekProps) {
  const [week, setWeek] = useState(_week);
    let _data = sessions.flatMap(o => o.presses)
      .filter(o => o.timestamp.getFullYear() == year)
      .filter(o => getWeek(o.timestamp) == week);

    let datesInWeek = _data.map(o => new Date(o.timestamp.getUTCFullYear(), o.timestamp.getUTCMonth(), o.timestamp.getUTCDate())).filter((date, i, self) => 
      self.findIndex(d => d.getTime() === date.getTime()) === i
    );


    let activities = datesInWeek.flatMap(o => GetGapIntersectForDate<ActivitySpan>(sessions.flatMap(s => s.activitiesSpan), o).map(d => ({...d, 'dayInWeek': o.getDay()})));
    let nonwear = datesInWeek.flatMap(o => GetGapIntersectForDate<Gaps>(sessions.flatMap(s => s.gaps), o).map(d => ({...d, 'dayInWeek': o.getDay()})));
    console.log("GAPSSE", activities, nonwear);
    console.log(timeFloat(nonwear[0].start), timeFloat(nonwear[0].end));


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
          Plot.barY(datesInWeek, {
            y1: 0,
            y2: 23.59,
            x: (d) => d.getDay(),
            fill: 'lightblue'
          }),
          Plot.barY(activities.filter(o => o.activity === 'still'), {
            y1: (d) => timeFloat(new Date(d.start)),
            y2: (d) => timeFloat(new Date(d.end)),
            x: 'dayInWeek',
            fill: 'lightgreen',
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
          Plot.barY(nonwear, {
            y1: (d) => timeFloat(d.start),
            y2: (d) => timeFloat(d.end),
            x: 'dayInWeek',
            fill: 'lightgray',
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
        <Col style={{display: 'flex', gap: 10, alignItems: 'center'}}>
          <><SquareFill color='lightgray'/>Non wear</>
          <><SquareFill color='lightgreen'/>Still wear</>
          <><SquareFill color='lightblue'/>Active wear</>
        </Col>
        <Col style={{display: 'flex', gap: 10, alignItems: 'center', justifyContent: 'flex-end'}}>
          <Button variant='link' onClick={() => onMonthClick(datesInWeek[0].getMonth())} style={{color:'#000'}}>Month</Button>
        </Col>
      </Row>
      <Row>
        <Col>
          <div ref={containerRef}/>
        </Col>
      </Row>
    </Container>
}

export default CalendarWeek;