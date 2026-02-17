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
          <PicksTable seasonId={activeSeason?.id}/>
        </Grid>
      </Grid>
    </Box>
  )
};

export default ParticipantPicks;