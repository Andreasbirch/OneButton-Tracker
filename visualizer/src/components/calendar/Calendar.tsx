import React, { useEffect, useRef, useState } from 'react';
import CalendarMonth from './month/CalendarMonth';
import CalendarWeek from './week/CalendarWeek';
import CalendarDay from './day/CalendarDay';
import CalendarYear from './year/CalendarYear';
import CalendarDayHorizontal from './day/CalendarDayHorizontal';
import { Col, Container, Row } from 'react-bootstrap';

type Props = {
    year?: number, 
    month?: number,
    week?: number,
    day?: number
}

type Scope = 'year' | 'month' | 'week' | 'day';


function Calendar() {
    let today = new Date();
    let year = today.getFullYear() - 1;
    
    const [scope, setScope] = useState<Scope>('year');
    const [selectedYear, setSelectedYear] = useState<number | null>(today.getFullYear() - 1);
    const [selectedMonth, setSelectedMonth] = useState<number | null>(null);
    const [selectedWeek, setSelectedWeek] = useState<number | null>(null);
    const [selectedDay, setSelectedDay] = useState<number | null>(null);

    const handleMonthClick = (month: number) => {
        setSelectedMonth(month);
        setScope('month');
    };

    const handleWeekClick = (year: number, week: number) => {
        setSelectedYear(year);
        setSelectedWeek(week);
        setScope('week');
    };

    const handleDateClick = (year:number, month: number, date: number) => {
        setSelectedYear(year);
        setSelectedMonth(month);
        setSelectedDay(date);
        setScope('day');
    };

    const colRef = useRef<HTMLDivElement>(null); // Ref to access Col's DOM node
    const [colWidth, setColWidth] = useState<number>(0); // State to store width

    useEffect(() => {
        if (colRef.current) {
            setColWidth(colRef.current.offsetWidth); // Set the initial width
        }

        const handleResize = () => {
            if (colRef.current) {
                setColWidth(colRef.current.offsetWidth); // Update width on resize
            }
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return <>
        <Container>
            <Row>
                <Col ref={colRef}>
                </Col>
            </Row>
        </Container>
        <CalendarYear
            year={year} 
            onMonthClick={handleMonthClick}
            onWeekClick={handleWeekClick}
            onDateClick={handleDateClick}></CalendarYear>
            <>
                { scope == 'month' && selectedMonth && (<CalendarMonth year={year} month={selectedMonth} onWeekClick={handleWeekClick} onDateClick={handleDateClick}></CalendarMonth>)}
                { scope == 'week' && selectedWeek && (<CalendarWeek year={year} week={selectedWeek} width={colWidth}></CalendarWeek>)}
                {/* {selectedYear && selectedMonth && selectedDay && (<CalendarDay year={year} month={selectedMonth} date={selectedDay}></CalendarDay>)} */}
                { scope == 'day' && selectedYear && selectedMonth && selectedDay && (<CalendarDayHorizontal year={year} month={selectedMonth} date={selectedDay} width={colWidth}></CalendarDayHorizontal>)}
            </>
    </>
}

export default Calendar;