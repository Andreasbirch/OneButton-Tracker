import React, { useState } from 'react';
import { getColor, getDaysArray, getWeek, groupBy } from '../helpers';
import { Button, ButtonGroup, Col, Container, Row, Table } from 'react-bootstrap';
import { ChevronLeft, ChevronRight } from 'react-bootstrap-icons';
import { Scope } from '../../../models/enums';
import { Session } from '../../../models/patients/PatientData';
import SideBar from '../../../../src/components/sidebar/sideBar';

type CalendarYearProps = {
    scope: Scope;
    setScope: (scope: Scope) => void;
    selectedMonth: number | null;
    selectedWeek: number | null;
    selectedDate: number | null;
    sessions: Session[];
    allSessions: Session[];
    onSessionsSelected: (sessions: Session[]) => void;
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

function CalendarYear({scope, setScope, selectedMonth, selectedWeek, selectedDate, sessions, allSessions, onSessionsSelected, onMonthClick, onWeekClick, onDateClick}: CalendarYearProps) {
    console.log(scope, selectedMonth, selectedWeek, selectedDate);
    const [year, setYear] = useState(new Date().getFullYear())

    const increment = () => {
        if (scope === Scope.Year) setYear(year + 1);
        else if (scope === Scope.Month && selectedMonth !== null) onMonthClick((selectedMonth + 1) % 12);
        else if (scope === Scope.Week && selectedWeek !== null) onWeekClick(year, selectedWeek + 1);
        else if (scope === Scope.Day && selectedDate !== null) onDateClick(year, selectedMonth, selectedDate + 1);
    };

    const decrement = () => {
        if (scope === Scope.Year) setYear(year - 1);
        else if (scope === Scope.Month && selectedMonth !== null) onMonthClick((selectedMonth - 1 + 12) % 12);
        else if (scope === Scope.Week && selectedWeek !== null) onWeekClick(year, selectedWeek - 1);
        else if (scope === Scope.Day && selectedDate !== null) onDateClick(year, selectedMonth, selectedDate - 1);
    };

    let data = sessions.flatMap(o => o.presses).filter(o => o.timestamp.getFullYear() == year);
    let groups = groupBy(data, o => o.timestamp.toISOString().split('T')[0]);

    return <Container fluid={true} id='calendar-year'>
        <Row>
            <Col style={{ display: 'flex', justifyContent: 'center' }}>
                <ButtonGroup className='date-navigator-group' style={{ alignItems: 'center' }}>
                    <Button className='btn btn-light' onClick={decrement}><ChevronLeft /></Button>
                    
                    <div className='h3 bg-light' style={{ marginBottom: 0 }}>
                        {scope == Scope.Day && (
                            <><span role="button" onClick={() => onDateClick(year, selectedMonth, selectedDate)}>{selectedDate}</span>{" "}
                            <span role="button" onClick={() => onMonthClick(selectedMonth)}>{months[selectedMonth]}{" "}</span></>
                        )}
                        {scope == Scope.Week && (
                            <><span role="button" onClick={() => onWeekClick(year, selectedMonth)}>Week {selectedWeek}</span>{" "}</>
                        )}
                        {scope == Scope.Month && (
                            <><span role="button" onClick={() => onMonthClick(selectedMonth)}>{months[selectedMonth]}</span>{" "}</>
                        )}
                        <span role="button" onClick={() => setScope(Scope.Year)}>{year}</span>
                    </div>

                    <Button className='btn btn-light' onClick={increment}><ChevronRight /></Button>
                </ButtonGroup>
            </Col>
        </Row>
        <SideBar _sessions={allSessions} onSessionsSelected={onSessionsSelected}></SideBar>
        <Row style={{ display: 'flex', flexWrap: 'nowrap', overflowX: 'auto' }}>
            {months.map((m, i) => {
                let calendar = GetCalendar(year, i);
                return (
                    <Col key={i} style={{ flex: '1 1 auto', padding: '5px' }}>
                        <Table className='table-fit' bordered>
                            <caption className='calendar-month' role='button' style={{ captionSide: 'top', textAlign: 'left' }} onClick={() => onMonthClick(i) }>{m}</caption>
                            <thead>
                                <tr>
                                    {['','m', 't', 'w', 't', 'f', 's', 's'].map((d, idx) => (
                                        <th style={{fontWeight: 'lighter', fontSize: 10}} key={idx}>{d.toUpperCase()}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {Object.keys(calendar).map((k) => (
                                    <tr key={k}>
                                        <td role='button' onClick={() => onWeekClick(year, parseInt(k))}>
                                            {k}
                                        </td>
                                        {calendar[k].map((o: Date, idx: number) => {
                                            if (!o) return <td key={idx}></td>;
                                            let colr = getColor(groups, new Date(new Date(o).setDate(o.getDate() + 1)));
                                            // console.log(color);
                                            return (
                                                <td
                                                    className={`table-day ${colr? '' : 'disabled'}`}
                                                    key={`${k}-${idx}`}
                                                    role="button"
                                                    style={{ backgroundColor: colr ?? '', color: colr? '#000' : '#BBB' , fontSize: 12 }}
                                                    onClick={() =>
                                                        colr? onDateClick(o?.getFullYear(), o?.getMonth(), o?.getDate()) : null
                                                    }
                                                >
                                                    {o?.getDate()}
                                                </td>
                                            );
                                        })}
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    </Col>
                );
            })}
        </Row>


        {/* <Row>
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
        </Row> */}
    </Container>
}

export default CalendarYear;