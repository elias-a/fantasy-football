import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Teams() {
    const [managers, setManagers] = useState(null);

    useEffect(() => {
        axios.post('/api/get-managers', {}).then(res => {
            setManagers(res.data);
        });
    }, []);

    return (
        <div>
            {managers !== null && Object.keys(managers).map(manager => {
                return (
                    <li 
                        key={manager}
                    >
                        {managers[manager]}
                    </li>
                );
            })}
        </div>
    );
}

export default Teams;