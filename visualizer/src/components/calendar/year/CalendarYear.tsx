import React from 'react';
import { getColor, getDaysArray, getWeek, groupBy } from '../helpers';
import mockdatapresses from '../../../mock_data_presses.json';
import { Col, Container, Row, Table } from 'react-bootstrap';

function GetCalendar(year: number) {
    let firstDate = new Date(year, 0, 1);
    let lastDate = new Date(year, 11, 31);
    let daysInYear = getDaysArray(firstDate, lastDate);
    let firstDateInYear = daysInYear.shift()!;

    
    // Group every date into weeks
    let calendar: {week: number, dates: Date[]}[] = [];
    let currentWeek = {week: getWeek(firstDateInYear), dates: [firstDateInYear]};
    daysInYear.forEach(date => {
        let week = getWeek(date);
        if(week !== currentWeek.week) {
            calendar.push(currentWeek);
            currentWeek = {week, dates: []};
        }
        currentWeek.dates.push(date);
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

function CalendarYear({year}: {year:number}) {
    let data = mockdatapresses.map(o => ({timestamp: new Date(o.timestamp), duration: o.duration}))
        .filter(o => o.timestamp.getFullYear() == year);
    let groups = groupBy(data, o => o.timestamp.toISOString().split('T')[0]);
    let [calendar, weekSpans] = GetCalendar(year);
    
    let datesForWeekdays = ['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((_,i) => 
        calendar.map(o => o.dates[i])
    );
    console.log(groups);
    return <Container id='calendar-year'>
        <Row>
            <Col>
                <Table responsive={true} bordered={true}>
                    <thead>
                        <tr>
                            <th></th>
                            {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].map((m,i) => {
                                return <th scope='col' className='month-name' colSpan={weekSpans[i]}>{m}</th>
                            })}
                        </tr>
                    </thead>
                    <tbody>
                        <tr className='week-numbers'>
                            <th scope='row'></th>
                            {
                                Object.keys(calendar).map(o => <td className='text-muted text-sm small-font-size' >{(parseInt(o) % 52) + 1}</td>)
                            }
                        </tr>
                        {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((m, i) => {
                            return <tr>
                                <th scope='row' className='week-day'>
                                    {m}
                                </th>
                                {datesForWeekdays[i].map(o => 
                                    <td className='week-date' 
                                        style={{backgroundColor: getColor(groups, o)?? "", 
                                            borderTop: (o?.getMonth() > 0 && o?.getDate() == 1 && o?.getDay() != 1)? "2px solid black" : "2px solid lightgray",
                                            borderLeft: (o?.getMonth() > 0 && o?.getDate() <= 7) ? "2px solid black" : ""
                                        }}>
                                        {o?.getDate()}
                                    </td>)}
                            </tr>
                        })}
                    </tbody>
                </Table>
            </Col>
        </Row>
    </Container>
}

export default CalendarYear;