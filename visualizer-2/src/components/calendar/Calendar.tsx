import React, { useEffect, useRef, useState } from 'react';
import CalendarMonth from './month/CalendarMonth';
import CalendarWeek from './week/CalendarWeek';
import CalendarYear from './year/CalendarYear';
import CalendarDayHorizontal from './day/CalendarDayHorizontal';
import { Col, Container, Row } from 'react-bootstrap';
import { Scope } from '../../models/enums';
import SideBar from '../sidebar/sideBar';
import { PatientRepository } from '../../managers/PatientRepository';
import { Session } from '../../models/patients/PatientData';


function Calendar({selectedDeviceId}: {selectedDeviceId: string}) {
    let today = new Date();
    let year = today.getFullYear();
    
    const patientDataManager = new PatientRepository();
    const patientData = patientDataManager.getPatientData(selectedDeviceId);

    console.log("Patient data for id " + selectedDeviceId, patientData);

    const [scope, setScope] = useState<Scope>(Scope.Year);
    const [selectedYear, setSelectedYear] = useState<number | null>(year);
    const [selectedMonth, setSelectedMonth] = useState<number | null>(null);
    const [selectedWeek, setSelectedWeek] = useState<number | null>(null);
    const [selectedDay, setSelectedDay] = useState<number | null>(null);
    const [selectedSessions, setSelectedSessions] = useState<Session[]>(patientData.sessions);

    const handleMonthClick = (month: number) => {
        setSelectedMonth(month);
        setScope(Scope.Month);
    };

    const handleWeekClick = (year: number, week: number) => {
        setSelectedYear(year);
        setSelectedWeek(week);
        setScope(Scope.Week);
    };

    const handleDateClick = (year:number, month: number, date: number) => {
        console.log("DateClick", year, month, date);
        setSelectedYear(year);
        setSelectedMonth(month);
        setSelectedDay(date);
        setScope(Scope.Day);
    };

    const handleSelectedSessionsUpdate = (sessions: Session[]) => {
        console.log("Selected sessions", sessions);
        setSelectedSessions(sessions);
    }

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
        <Container fluid={true}>
            <Row>
                <Col>
                    <CalendarYear
                        onMonthClick={handleMonthClick}
                        onWeekClick={handleWeekClick}
                        onDateClick={handleDateClick}
                        onSessionsSelected={handleSelectedSessionsUpdate}
                        scope={scope}
                        setScope={setScope}
                        selectedMonth={selectedMonth}
                        selectedWeek={selectedWeek}
                        selectedDate={selectedDay}
                        sessions={selectedSessions}
                        allSessions={patientData.sessions}></CalendarYear>
                        { scope == Scope.Month && selectedMonth && (<CalendarMonth year={year} _month={selectedMonth} sessions={selectedSessions} onWeekClick={handleWeekClick} onDateClick={handleDateClick}></CalendarMonth>)}
                        { scope == Scope.Week && selectedWeek && (<CalendarWeek year={year} _week={selectedWeek} width={colWidth} sessions={selectedSessions} onMonthClick={handleMonthClick}></CalendarWeek>)}
                        {/* {selectedYear && selectedMonth && selectedDay && (<CalendarDay year={year} month={selectedMonth} date={selectedDay}></CalendarDay>)} */}
                        { scope == Scope.Day && selectedYear && selectedMonth && selectedDay && (<CalendarDayHorizontal year={year} month={selectedMonth} _date={selectedDay} width={colWidth} sessions={selectedSessions} onWeekClick={handleWeekClick} onMonthClick={handleMonthClick}></CalendarDayHorizontal>)}
                </Col>
            </Row>
        </Container>
    </>
}

export default Calendar;