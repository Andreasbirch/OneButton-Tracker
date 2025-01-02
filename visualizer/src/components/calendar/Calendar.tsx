import React from 'react';
import mockdatapresses from '../../mock_data_presses.json';
import {Scope} from '../../models/enums';
import { Container, Row, Col } from 'react-bootstrap';
import { groupBy, getWeek } from '../../components/calendar/helpers'
import CalendarMonth from './CalendarMonth';

type Props = {
    year?: number, 
    month?: number,
    week?: number,
    day?: number
}

type CalendarItem = {
    timestamp: Date,
    duration: number
}



function GetCalendarMonth(year: number, month: number) {
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

function GetCalendarWeek(year: number, week:number) {
    
}

function Calendar({year, month, week, day}: Props) {
    var calendar: any;

    return <>
        <Container>
            <Row>
                <Col>
                    <p>Month</p>
                </Col>
            </Row>
        </Container>
        <Container>
            <Row>
                <Col>
                    <CalendarMonth year={year!} month={month!}></CalendarMonth>
                </Col>
            </Row>
        </Container>
    </>
}

export default Calendar;