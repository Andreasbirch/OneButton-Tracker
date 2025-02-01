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

function GetCalendar(year: number, month: number) {
    let firstDayInMonth = new Date(year, month, 1);
    let lastDayInMonth = new Date(year, month + 1, 0);

    let firstWeekInMonth = getWeek(firstDayInMonth);
    let lastWeekInMonth = getWeek(lastDayInMonth);

    let weeks = {} as any;
    for (let i = firstWeekInMonth; i <= (lastWeekInMonth == 1 ? 52 : lastWeekInMonth); i++) {
        weeks[i] = new Array(7).fill(null);
    }
    weeks[lastWeekInMonth] = new Array(7).fill(null);
    
    for (let i = firstDayInMonth.getDate(); i <= lastDayInMonth.getDate(); i++) {
        let date = new Date(year, month, i);
        weeks[getWeek(date)][(date.getDay() + 6) % 7] = date;
    }
    return weeks;
}

const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

function CalendarYear({scope, selectedMonth, selectedWeek, selectedDate, sessions, onMonthClick, onWeekClick, onDateClick}: CalendarYearProps) {
    console.log(scope, selectedMonth, selectedWeek, selectedDate);
    const [year, setYear] = useState(new Date().getFullYear())

    let data = sessions.flatMap(o => o.presses).filter(o => o.timestamp.getFullYear() == year);
    let groups = groupBy(data, o => o.timestamp.toISOString().split('T')[0]);

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
            <div className='compact-calendar-container'>
            {months.map((m,i) => {
                let calendar = GetCalendar(year, i);
                return <Col className='compact-calendar-month'>
                    <div className="calendar-month" role='button' onClick={() => onMonthClick(i)}>{m}</div>
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
            })}
            </div>
        </Row>
    </Container>
}

export default CalendarYear;