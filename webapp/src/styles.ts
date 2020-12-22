import { makeStyles } from '@material-ui/core/styles';

export const useStyles = makeStyles({
    container: {
        backgroundColor: '#fff',
        border: '4px solid #e6eeff',
        width: '50%',
        padding: '10px',
        margin: '40px auto',
    },
    data: {
        backgroundColor: '#99bbff',
        width: '90%',
        margin: '10px auto',
        padding: '10px',
        fontSize: '24px',
        color: '#fff',
    },
    button: {
        background: 'linear-gradient(45deg, #80aaff 30%, #4d88ff 90%)',
        border: 0,
        borderRadius: 3,
        boxShadow: '0 3px 5px 2px rgba(255, 105, 135, 0.3)',
        color: '#fff',
        height: 48, 
        width: '100%',
        padding: '0 30px',
        margin: '20px auto',
        display: 'block',
    },
    form: {
        display: 'block', 
        width: '40%',
        margin: '20px auto',
    },
    input: {
        display: 'block',
        width: '100%',
        margin: '20px auto',
    },
});