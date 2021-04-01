import { makeStyles, createStyles } from '@material-ui/core/styles';

export const useStyles = makeStyles((theme) => createStyles({
    leagueDashboard: {
        width: '100vw',
        height: '100vh',
        position: 'absolute',
        top: 0,
        left: 0,
        backgroundColor: theme.palette.secondary.main,
    },
    teamsTableSection: {
        width: '36vw',
        height: '80vh',
        position: 'absolute',
        top: 0,
        left: 0,
        paddingTop: '20vh',
        paddingLeft: '4vw',
    },
    teamsTable: {
        border: '1px solid #000',
        borderCollapse: 'collapse',
    },
    teamsCell: {
        border: '1px solid #000',
        borderCollapse: 'collapse',
        width: '18vw',
        height: '5vh',
        textAlign: 'center',
    },
}));