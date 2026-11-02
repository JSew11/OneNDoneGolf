import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsTable from './seasonsTable';
import NewSeasonModal from 'src/assets/modals/newSeason'

const Seasons = () => {
  return (
    <Box sx={{ flexGrow: 1, textAlign: 'center'}}>
      <Grid container className='my-3 px-2'>
        <Grid item xs={10}></Grid>
        <Grid item xs={2}><NewSeasonModal /></Grid>
      </Grid>
      <Grid container className='px-2'>
        <Grid item xs={12}>
          <SeasonsTable />
        </Grid>
      </Grid>
    </Box>
  );
}

export default Seasons;