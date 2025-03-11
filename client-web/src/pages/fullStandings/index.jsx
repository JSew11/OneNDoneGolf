import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsApi from 'src/api/season';
import QuickStandingsTable from 'src/assets/components/quickStandingsTable';
import TournamentStandingsTable from '../../assets/components/tournamentStandingsTable';

const FullStandings = () => {
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
      <Box sx={{ flexGrow: 1 }}>
        <Grid container justifyContent='left' alignItems='center' className='px-2'>
          <Grid item xs={5}>
            <QuickStandingsTable seasonId={activeSeason?.id}/>
          </Grid>
          <Grid item xs={7}>
            <TournamentStandingsTable seasonId={activeSeason?.id} />
          </Grid>
        </Grid>
      </Box>
  );
}

export default FullStandings;