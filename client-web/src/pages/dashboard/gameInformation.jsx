import { useTheme } from '@mui/material';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

const GameInformation = () => {
  const theme = useTheme();

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container className='py-3 justify-content-center'
            sx={{ borderBottom: 2, borderColor: theme.palette.primary.dark }}>
        <Grid>
          <h1 className='playfair-display'>Want to Join the Game?</h1>
        </Grid>
      </Grid>
    </Box>
  );
}

export default GameInformation;