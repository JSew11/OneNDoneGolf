import { useTheme } from '@mui/material';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

const GameInformation = () => {
  const theme = useTheme();

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container justifyContent='center' alignItems='center' className='py-3'
            sx={{ borderBottom: 2, borderColor: theme.palette.primary.dark }}>
        <Grid item>
          <h1 className='playfair-display'>Want to Join the Game?</h1>
        </Grid>
      </Grid>
    </Box>
  );
}

export default GameInformation;