import React, { useEffect, useState } from 'react';
import { Button, ButtonGroup } from 'react-bootstrap/esm';
import { Session } from '../../models/patients/PatientData';

function SideBar({_sessions, onSessionsSelected}:{_sessions: Session[], onSessionsSelected: (sessions: Session[]) => void}) {
    const [sessions, setSessions] = useState<Session[]>(_sessions);
    const [selected, setSelected] = useState<number[]>([_sessions[_sessions.length - 1].id]);

    useEffect(() => {
        onSessionsSelected([_sessions[_sessions.length - 1]]);
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
        <ButtonGroup vertical role='group' style={{marginTop: 40, display: 'flex'}}>
            {sessions.map(s => {
                return <Button key={s.id} type='button' variant={selected.includes(s.id)? "secondary" : "outline-secondary"} style={{marginBottom: 20}} onClick={() => toggleButton(s.id)}>
                    <div>Session {s.id + 1}</div>
                    <div>{s.presses[0].timestamp.toDateString()} {s.presses[s.presses.length - 1].timestamp.toDateString()}</div>
                </Button>
            }).reverse()}
        </ButtonGroup>
    </>
}

export default SideBar;