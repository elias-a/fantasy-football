import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
    XYPlot,
    XAxis,
    YAxis,
    LineMarkSeries,
    VerticalBarSeries,
    LineSeries,
} from 'react-vis';
import { useStyles } from './styles';
import '../node_modules/react-vis/dist/style.css';

function League() {
    const [managers, setManagers] = useState(null);
    const [teams, setTeams] = useState(null);
    const [scores, setScores] = useState(null);
    const [plotData, setPlotData] = useState(null);
    const [averageWeeklyScores, setAverageWeeklyScores] = useState(null);
    const [averageErrorBars, setAverageErrorBars] = useState(null);
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
        const arrAvg = arr => arr.reduce((a,b) => a + b, 0) / arr.length;

        const data = [];
        const averages = [];
        const errorBars = [];
        Object.keys(scoreData).map((week: string) => {
            data.push({
                x: parseInt(week), 
                y: scoreData[week][team]
            });

            const averageScore = arrAvg(Object.values(scoreData[week]));
            averages.push({
                x: parseInt(week),
                y: averageScore
            });

            const squaredDifferences = Object.values(scoreData[week]).map((score: number) => {
                return Math.pow(score - averageScore, 2);
            });
            const std = Math.sqrt(arrAvg(squaredDifferences));

            errorBars.push({
                lower: averageScore - std,
                upper: averageScore + std
            });
        });

        setPlotData(data);
        setAverageWeeklyScores(averages);
        setAverageErrorBars(errorBars);
    };

    return (
        <div className={styles.leagueDashboard}>
            {selectedTeam !== '' && <React.Fragment>
                <div className={styles.teamsTableSection}>
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
                    </table>
                </div>

                <div className={styles.teamDashboardSection}>
                    <div 
                        style={{
                            paddingLeft: '5vw',
                            paddingTop: '10vh',
                            height: '40vh'
                        }}
                    >
                        <XYPlot width={650} height={300}>
                            <XAxis />
                            <YAxis />
                            
                            <VerticalBarSeries 
                                color={'#87CEFA'}
                                data={averageWeeklyScores}
                            />
                            {averageErrorBars.map((data: any, i: number) => { 
                                return <LineSeries
                                    color={'red'}
                                    data={[{
                                        x: i + 1,
                                        y: data.lower
                                    }, {
                                        x: i + 1,
                                        y: data.upper
                                    }]}
                                />
                            })}
                            <LineMarkSeries
                                color={'#0000CD'}
                                data={plotData}
                            />
                        </XYPlot>
                    </div>
                </div>
            </React.Fragment>}
        </div>
    );
}

export default League;