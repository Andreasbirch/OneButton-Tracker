import React, { useEffect, useState } from 'react';
import { Button, ButtonGroup } from 'react-bootstrap/esm';
import { Session } from '../../models/patients/PatientData';
import { CalendarRange } from 'react-bootstrap-icons/dist';

function SideBar({_sessions, onSessionsSelected}:{_sessions: Session[], onSessionsSelected: (sessions: Session[]) => void}) {
    const [sessions, setSessions] = useState<Session[]>(_sessions);
    const [selected, setSelected] = useState<number[]>([_sessions[_sessions.length-1].id]);

    useEffect(() => {
        onSessionsSelected([_sessions[_sessions.length-1]]);
    }, []);

    const toggleButton = (sessionId: number) => {
        let selectedIndices = [...selected];
        if (selectedIndices.includes(sessionId)) {
            selectedIndices = selectedIndices.filter(o => o!=sessionId);
        } else {
            selectedIndices.push(sessionId);
        }
        setSelected(selectedIndices);

        const updatedSessions = _sessions.filter(s => selectedIndices.includes(s.id))
        console.log("Sidebar, updated sessions: ", updatedSessions);
        onSessionsSelected(updatedSessions);
    };
    
    return <> 
        <ButtonGroup role="group" style={{ display: "flex", gap: 5 }}>
            {sessions.map((s) => {
                const start = s.presses[0].timestamp;
                const end = s.presses[s.presses.length - 1].timestamp;

                const formatDate = (date: Date, includeYear = true) =>
                `${date.getDate()}/${date.getMonth() + 1}${includeYear ? `/${date.getFullYear()}` : ""}`;

                const sameYear = start.getFullYear() === end.getFullYear();
                const dateRange = sameYear ? `${formatDate(start, false)} - ${formatDate(end, false)}`
                                           : `${formatDate(start)} - ${formatDate(end)}`;

                return (
                <Button
                    key={s.id}
                    type="button"
                    variant={selected.includes(s.id) ? "secondary" : "outline-secondary"}
                    style={{ height: 'fit-content', maxWidth: 350 }}
                    onClick={() => toggleButton(s.id)}
                >
                    <div className="d-flex align-items-center">
                    <div className="me-2">
                        <CalendarRange />
                    </div>

                    <div className="d-flex align-items-stretch" style={{width: '80%', justifyContent: 'space-between'}}>
                        <div>Session {s.id + 1}</div>
                        <div>{dateRange}</div>
                    </div>
                    </div>
                </Button>
                );
            })}
        </ButtonGroup>
    </>
}

export default SideBar;