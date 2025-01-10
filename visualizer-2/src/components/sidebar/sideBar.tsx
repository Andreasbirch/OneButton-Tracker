import React, { useState } from 'react';
import { Button, ButtonGroup } from 'react-bootstrap/esm';

function SideBar() {
    const allSessions = [1,2,3].reverse();
    const [sessions, setSessions] = useState<number[]>(allSessions);
    const [selected, setSelected] = useState<{[k: number]: boolean}>(Object.fromEntries(allSessions.map((x,i) => [x, i === 0])));

    const toggleButton = (buttonKey: number) => {
        setSelected(prevState => ({
          ...prevState,
          [buttonKey]: !prevState[buttonKey],
        }));
    };
    
    return <> 
        <ButtonGroup vertical role='group' style={{marginTop: 40, display: 'flex'}}>
            {sessions.map(s => {
                return <Button key={s} type='button' variant={selected[s]? "secondary" : "outline-secondary"} style={{marginBottom: 20}} onClick={() => toggleButton(s)}>
                    <div>Session {s}</div>
                    <div>2024-01-01 2024-03-1</div>
                </Button>
            })}
        </ButtonGroup>
    </>
}

export default SideBar;