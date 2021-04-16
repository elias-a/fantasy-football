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
import '../node_modules/react-vis/dist/style.css';
import { useStyles } from './styles';
import {
    average,
    standardError,
    median,
} from './helpers';

function League() {
    const [managers, setManagers] = useState(null);
    const [teams, setTeams] = useState(null);
    const [scores, setScores] = useState(null);
    const [plotData, setPlotData] = useState(null);
    const [averageWeeklyScores, setAverageWeeklyScores] = useState(null);
    const [averageErrorBars, setAverageErrorBars] = useState(null);
    const [medianWeeklyScores, setMedianWeeklyScores] = useState(null);
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
        const averages = [];
        const errorBars = [];
        const medians = [];
        Object.keys(scoreData).map((week: string) => {
            const scores = Object.values(scoreData[week]);

            data.push({
                x: parseInt(week), 
                y: scoreData[week][team]
            });

            const averageScore = average(scores);
            averages.push({
                x: parseInt(week),
                y: averageScore
            });

            const standardErrorScore = standardError(scores);
            errorBars.push({
                lower: averageScore - standardErrorScore,
                upper: averageScore + standardErrorScore
            });

            const medianScore = median(scores);
            medians.push({
                x: parseInt(week),
                y: medianScore
            });
        });

        setPlotData(data);
        setAverageWeeklyScores(averages);
        setAverageErrorBars(errorBars);
        setMedianWeeklyScores(medians);
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
                                    <td className={styles.teamsCell}
                                    style={{
                                        width: '10vw'
                                    }}
                                    >
                                        {managers[team]}
                                    </td>
                                    <td 
                                        className={styles.teamsCell}
                                        style={team === selectedTeam ? 
                                            { width: '26vw', backgroundColor: '#1d262b', color: '#fffff0' } 
                                            : { width: '26vw' }
                                        }
                                    >
                                        <button
                                            name={team}
                                            onClick={changeSelectedTeam}
                                            className={styles.teamButton}
                                            style={{
                                                width: '26vw'
                                            }}
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
                                color={'#89cff0'}
                                data={averageWeeklyScores}
                            />
                            <VerticalBarSeries
                                color={'#57a0d3'}
                                data={medianWeeklyScores}
                            />
                            {averageErrorBars.map((data: any, i: number) => { 
                                return <LineSeries
                                    color={'#d92121'}
                                    data={[{
                                        x: i + 0.8,
                                        y: data.lower
                                    }, {
                                        x: i + 0.8,
                                        y: data.upper
                                    }]}
                                />
                            })}
                            <LineMarkSeries
                                color={'#0f52ba'}
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