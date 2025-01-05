import React, { useState } from 'react';
import { groupBy, getWeek, getColor } from '../helpers';
import mockdatapresses from '../../../mock_data_presses.json';
import { Button, ButtonGroup, Col, Container, Row } from 'react-bootstrap';
import { ChevronLeft, ChevronRight } from 'react-bootstrap-icons';

type CalendarMonthProps = {
    year: number;
    _month: number;
    onWeekClick: (year:number, week: number) => void;
    onDateClick: (year: number, month: number, date: number) => void;
}
const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

function GetCalendar(year: number, month: number) {
    let firstDayInMonth = new Date(year, month, 1);
    let lastDayInMonth = new Date(year, month + 1, 0);

    let firstWeekInMonth = getWeek(firstDayInMonth);
    let lastWeekInMonth = getWeek(lastDayInMonth);

    let weeks = {} as any;
    for (let i = firstWeekInMonth; i <= lastWeekInMonth; i++) {
        weeks[i] = new Array(7).fill(null);
    }
    
    for (let i = firstDayInMonth.getDate(); i <= lastDayInMonth.getDate(); i++) {
        let date = new Date(year, month, i);
        weeks[getWeek(date)][(date.getDay() + 6) % 7] = date;
    }
    return weeks;
}

function CalendarMonth({year, _month, onWeekClick, onDateClick}:CalendarMonthProps) {
    const [month, setMonth] = useState(_month)
    var data = mockdatapresses.map(o => ({timestamp: new Date(o.timestamp), duration: o.duration}))
        .filter(o => o.timestamp.getFullYear() == year)
        .filter(o => o.timestamp.getMonth() == month);

    var groups = groupBy(data, o => o.timestamp.toISOString().split('T')[0]);

    console.log(data);
    var calendar = GetCalendar(year, month);
    console.log(calendar);
    return <Container id='calendar-month'>
    <Row>
        <Col style={{display: 'flex', justifyContent: 'center'}}>
            <ButtonGroup style={{alignItems: 'center'}}>
                <Button className='btn btn-light' onClick={() => setMonth(month - 1)}><ChevronLeft></ChevronLeft></Button>
                <div className='h3 bg-light' style={{marginBottom: 0}}>{months[month % 12]}</div>
                <Button className='btn btn-light' onClick={() => setMonth(month + 1)}><ChevronRight></ChevronRight></Button>
            </ButtonGroup>
        </Col>
    </Row>
    <Row>
      <Col>
        <div>
            <div className='calendar-header'>
                <div></div>
                <div>Mon</div>
                <div>Tue</div>
                <div>Wed</div>
                <div>Thu</div>
                <div>Fri</div>
                <div>Sat</div>
                <div>Sun</div>
            </div>
            {Object.keys(calendar).map(k => 
                <div className='calendar-week' key={k}>
                    <div className='week-number' key={`${k}-week`} role='button' onClick={() => onWeekClick(year, parseInt(k))}>{k}</div>
                    <div className='week-days'>
                        {calendar[k].map((o: Date, i:number) => 
                        {
                            if(!o) 
                                return <div className='week-day'></div>
                            return <div 
                                role='button'
                                className='week-day'
                                style={{backgroundColor: getColor(groups, o)?? ""}}
                                onClick={() => onDateClick(o?.getFullYear(), o?.getMonth(), o?.getDate())}
                                key={`${k}-${i}`}>{o?.getDate()}
                            </div>
                        })}
                    </div>
                </div>
            )}
        </div>
      </Col>
    </Row>
  </Container>
}

export default CalendarMonth;