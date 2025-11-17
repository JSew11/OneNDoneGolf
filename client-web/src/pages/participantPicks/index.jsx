import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsApi from 'src/api/season';
import PicksTable from 'src/assets/components/picksTable';

const ParticipantPicks = () => {

  const [activeSeason, setActiveSeason] = useState(null);

  const { isLoggedIn } = useSelector(state => state.auth);

  useEffect(() => {
    if (isLoggedIn) {
      SeasonsApi.active().then(
        (response) => {
          if (response.status === 200) {
            setActiveSeason(response.data);
          }
        },
        (error) => error
      );
    }
  }, [isLoggedIn]);

  return (
    <Box sx={{ flexGrow: 1 }} className='mt-3 px-2'>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          {
            activeSeason ?
              <PicksTable seasonId={activeSeason.id}/>
            :
              <h1>There is no currently active season. Please check in again while there is an ongoing event!</h1>
          }
        </Grid>
      </Grid>
    </Box>
  )
};

export default ParticipantPicks;