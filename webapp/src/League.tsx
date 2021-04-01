import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useStyles } from './styles';

function League() {
    const [managers, setManagers] = useState(null);
    const [teams, setTeams] = useState(null);
    const [selectedTeam, setSelectedTeam] = useState<string>('1');
    const styles = useStyles();

    useEffect(() => {
        axios.post('/api/get-team-data', {}).then(res => {
            setTeams(res.data.teams);
            setManagers(res.data.managers);
        });
    }, []);

    const changeSelectedTeam = (event) => {
        const { name } = event.target;
        setSelectedTeam(name);
    };

    return (
        <div className={styles.leagueDashboard}>
            <div className={styles.teamsTableSection}>
                {managers !== null && 
                <table 
                    className={styles.teamsTable}
                >
                    <tr>
                        <th className={styles.teamsCell}>
                            {'Manager'}
                        </th>
                        <th className={styles.teamsCell}>
                            {'Team'}
                        </th>
                    </tr>
                    {Object.keys(teams).map((team: string) => {
                        return (
                            <tr key={team}>
                                <td className={styles.teamsCell}>
                                    {managers[team]}
                                </td>
                                <td 
                                    className={styles.teamsCell}
                                    style={team === selectedTeam ? 
                                        { backgroundColor: '#fff' } 
                                        : null
                                    }
                                >
                                    <button
                                        name={team}
                                        onClick={changeSelectedTeam}
                                    >
                                        {teams[team]}
                                    </button>
                                </td>
                            </tr>
                        );
                    })}
                </table>}
            </div>
        </div>
    );
}

export default League;