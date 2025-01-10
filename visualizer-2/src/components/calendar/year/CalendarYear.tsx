import React, { useState } from 'react';
import { getColor, getDaysArray, getWeek, groupBy } from '../helpers';
import { Button, ButtonGroup, Col, Container, Row, Table } from 'react-bootstrap';
import { ChevronLeft, ChevronRight } from 'react-bootstrap-icons';
import { Scope } from '../../../models/enums';
import { Session } from '../../../models/patients/PatientData';

type CalendarYearProps = {
    scope: Scope;
    selectedMonth: number | null;
    selectedWeek: number | null;
    selectedDate: number | null;
    sessions: Session[];
    onMonthClick: (month: number) => void;
    onWeekClick: (year: number, week: number) => void;
    onDateClick: (year: number, month: number, date: number) => void;
}

function GetCalendar(year: number) {
    let firstDate = new Date(year, 0, 1);
    let lastDate = new Date(year, 11, 31);
    let daysInYear = getDaysArray(firstDate, lastDate);
    let firstDateInYear = daysInYear.shift()!;
    
    // Group every date into weeks
    //TODO: Der bliver fyldt forkert på her, det skal være index baseret på getDay()!!!
    let calendar: {week: number, dates: Date[]}[] = [];
    let currentWeek = {week: getWeek(firstDateInYear), dates: new Array(7).fill(undefined)};
    currentWeek.dates[(firstDateInYear.getDay() + 6) % 7] = firstDateInYear;
    daysInYear.forEach(date => {
        let week = getWeek(date);
        if(week !== currentWeek.week) {
            calendar.push(currentWeek);
            currentWeek = {week, dates: new Array(7).fill(undefined)};
        }
        currentWeek.dates[(date.getDay() + 6) % 7] = date;
    });
    calendar.push(currentWeek);



    // Get the amount of full weeks within a month
    let prevLastWeek = getWeek(new Date(year, 1, 0));
    let _weekSpans: number[] = [prevLastWeek];
    for (let month = 1; month < 12; month++) {
        let currentLastWeek = getWeek(new Date(year, month + 1, 0));
        _weekSpans.push(currentLastWeek);
    }
    let weekSpans = new Array(12);
    weekSpans[0] = _weekSpans[0];

    for (let month = 1; month < 11; month++) {
        weekSpans[month] = Math.abs(_weekSpans[month] - _weekSpans[month-1]);
    }
    weekSpans[11] = Math.abs(_weekSpans[10] - calendar.length);

    return [calendar, weekSpans];
}

function CalendarYear({scope, selectedMonth, selectedWeek, selectedDate, sessions, onMonthClick, onWeekClick, onDateClick}: CalendarYearProps) {
    console.log(scope, selectedMonth, selectedWeek, selectedDate);
    const [year, setYear] = useState(new Date().getFullYear())

    let data = sessions.flatMap(o => o.presses).filter(o => o.timestamp.getFullYear() == year);
    let groups = groupBy(data, o => o.timestamp.toISOString().split('T')[0]);
    let [calendar, weekSpans] = GetCalendar(year);
    
    let weekSpansAccumulated = weekSpans.map((sum => value => sum += value)(0));

    let datesForWeekdays = ['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((_,i) => 
        calendar.map(o => o.dates[i])
    );
    return <Container id='calendar-year'>
        <Row>
            <Col style={{display: 'flex', justifyContent: 'center'}}>
                <ButtonGroup style={{alignItems: 'center'}}>
                    <Button className='btn btn-light' onClick={() => setYear(year - 1)}><ChevronLeft></ChevronLeft></Button>
                    <div className='h3 bg-light' style={{marginBottom: 0}}>{year}</div>
                    <Button className='btn btn-light' onClick={() => setYear(year + 1)}><ChevronRight></ChevronRight></Button>
                </ButtonGroup>
            </Col>
        </Row>
        <Row>
            <Col>
                <div>
                    {/* Months Row */}
                    <div className='months' style={{
                        display: "grid",
                        gridTemplateColumns: `1em repeat(${calendar.length}, 1fr)`,
                        gridAutoRows: "2em",
                    }}>
                        <div></div>
                        {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].map((m, i) => (
                            <div 
                                key={m} 
                                style={{ gridColumn: `span ${weekSpans[i]}`, textDecoration: (scope == Scope.Month && i == selectedMonth) ? "underline" : "" }} 
                                role='button'
                                className='month-name'
                                onClick={() => onMonthClick(i)}>
                                {m}
                            </div>
                        ))}
                    </div>

                    {/* Weeks Row */}
                    <div className='weeks' style={{
                        display: "grid",
                        gridTemplateColumns: `1em repeat(${calendar.length}, 1fr)`,
                    }}>
                        <div></div>
                        {Object.keys(calendar).map(o => (
                            <div key={`week-${o}`} 
                                 role='button'
                                style={{
                                    fontWeight: (scope == Scope.Week && parseInt(o) == selectedWeek!-1) ? "bold" : "",
                                    borderLeft: (weekSpansAccumulated.includes(parseInt(o))) ? "2px solid var(--bs-gray-500)" : ""
                                }}
                                onClick={() => onWeekClick(year, parseInt(o) + 1)}>
                                {(parseInt(o) % 52) + 1}
                            </div>
                        ))}
                    </div>
                    <div style={{
                                display: 'grid',
                                gridTemplateRows: "repeat(7, 1fr)",
                                rowGap: 1
                            }}>
                        {/* Days and Dates Rows */}
                        {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((m, i) => (
                            <div key={`day-${i}`} className='week-row' style={{
                                display: 'grid',
                                gridTemplateColumns: `1em repeat(${calendar.length}, 1fr)`,
                            }}>
                                <div className='week-day'>{m}</div>
                                {datesForWeekdays[i].map((o, index) => (
                                    <div 
                                        key={`${o?.getFullYear()}-${o?.getMonth()}-${o?.getDate()}`}
                                        className='week-date' 
                                        role='button'
                                        onClick={() => onDateClick(o?.getFullYear(), o?.getMonth(), o?.getDate())}
                                        style={{
                                            fontWeight: (scope == Scope.Day && o?.getMonth() == selectedMonth && o?.getDate() == selectedDate) ? "bold" : "",
                                            backgroundColor: getColor(groups, o)?? "#eee", 
                                            borderTop: (o?.getMonth() > 0 && o?.getDate() == 1 && o?.getDay() != 1)? "2px solid var(--bs-gray-500)" : "",
                                            borderLeft: (o?.getMonth() > 0 && o?.getDate() <= 7) ? "2px solid var(--bs-gray-500)" : ""
                                        }}>
                                        {o?.getDate()}
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                </div>
            </Col>
        </Row>
    </Container>
}

export default CalendarYear;