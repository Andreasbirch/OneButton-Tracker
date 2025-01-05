import React from 'react';
import { groupBy, getWeek, getColor } from '../helpers';
import mockdatapresses from '../../../mock_data_presses.json';
import { Col, Container, Row } from 'react-bootstrap';

type CalendarMonthProps = {
    year: number,
    month: number
    onWeekClick: (year:number, week: number) => void;
    onDateClick: (year: number, month: number, date: number) => void;
}

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

function CalendarMonth({year, month, onWeekClick, onDateClick}:CalendarMonthProps) {
    var data = mockdatapresses.map(o => ({timestamp: new Date(o.timestamp), duration: o.duration}))
        .filter(o => o.timestamp.getFullYear() == year)
        .filter(o => o.timestamp.getMonth() == month);

    var groups = groupBy(data, o => o.timestamp.toISOString().split('T')[0]);

    console.log(data);
    var calendar = GetCalendar(year, month);
    console.log(calendar);
    return <Container id='calendar-month'>
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