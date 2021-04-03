import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
    XYPlot, 
    MarkSeries,
    XAxis,
    YAxis,
} from 'react-vis';
import { useStyles } from './styles';

function League() {
    const [managers, setManagers] = useState(null);
    const [teams, setTeams] = useState(null);
    const [scores, setScores] = useState(null);
    const [plotData, setPlotData] = useState([]);
    const [selectedTeam, setSelectedTeam] = useState<string>('');
    const styles = useStyles();

    useEffect(() => {
        axios.post('/api/get-team-data', {}).then(res => {
            setTeams(res.data.teams);
            setManagers(res.data.managers);
            setScores(res.data.scores);

            const team = Object.keys(res.data.teams)[0];
            changePlotData(res.data.scores, team); 
            setSelectedTeam(team);
        });
    }, []);

    const changeSelectedTeam = (event) => {
        const { name } = event.target;
        setSelectedTeam(name);
        changePlotData(scores, name);
    };

    const changePlotData = (scoreData, team: string) => {
        const data = [];
        Object.keys(scoreData[team]).map((week: string) => {
            data.push({
                x: parseInt(week), 
                y: scoreData[team][week]
            });
        });
        setPlotData(data);
    };

    return (
        <div className={styles.leagueDashboard}>
            <div className={styles.teamsTableSection}>
                {selectedTeam !== '' && 
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

            <div className={styles.teamDashboardSection}>
                <div 
                    style={{
                        paddingLeft: '10vw',
                        paddingTop: '10vh',
                        height: '90vh',
                    }}
                >
                    <XYPlot height={300} width={500}>
                        <XAxis />
                        <YAxis />
                        <MarkSeries data={plotData} />
                    </XYPlot>
                </div>
            </div>
        </div>
    );
}

export default League;