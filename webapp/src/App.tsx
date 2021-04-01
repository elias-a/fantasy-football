import React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import League from './League';
import { theme } from './theme';

function App() {
    return (
      <ThemeProvider theme={theme}>
        <div>
          <League />
        </div>
      </ThemeProvider>
    );
}

export default App;