import { makeStyles } from '@material-ui/core/styles';

export const useStyles = makeStyles({
    leagueDashboard: {
        width: '100vw',
        height: '100vh',
        position: 'absolute',
        top: 0,
        left: 0,
        backgroundColor: '#1d262b',
        color: '#1d262b',
        fontFamily: 'Tahoma'
    },
    teamsTableSection: {
        backgroundColor: '#3a70a6',
        width: '36vw',
        height: '80vh',
        position: 'absolute',
        top: 0,
        left: 0,
        padding: '20vh 2vw 0 2vw',
    },
    teamsTable: {
        border: 'none',
    },
    teamsCell: {
        border: 'none',
        height: '5vh',
        textAlign: 'center',
        backgroundColor: '#fffff0',
    },
    teamButton: {
        width: '18vw',
        height: '5vh',
        background: 'none',
        color: 'inherit',
        border: 'none',
        padding: 0,
        font: 'inherit',
        cursor: 'pointer',
        outline: 'inherit',
    },
    teamDashboardSection: {
        marginLeft: '40vw',
        width: '60vw',
        height: '100vh',
    }, 
});