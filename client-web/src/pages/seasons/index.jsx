import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import { useSelector } from 'react-redux';

const Seasons = () => {
  const { isLoggedIn } = useSelector(state => state.auth);

  return (
    <Box sx={{ flexGrow: 1, textAlign: 'center'}}>
      <Grid container className='mt-3 px-2'>
        <Grid item xs={12}>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Seasons;