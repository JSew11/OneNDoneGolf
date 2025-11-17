import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsApi from 'src/api/season';
import FullTournamentTable from 'src/assets/components/fullTournamentTable';

const WeeklyPicks = () => {

  const [activeSeason, setActiveSeason] = useState(null);
  const [isActiveTournament, setIsActiveTournament] = useState(true);
  const [activeTournament, setActiveTournament] = useState(null);
  
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

  useEffect(() => {
    if (activeSeason !== null) {
      SeasonsApi.activeTournament(activeSeason.id).then(
        (response) => {
          if (response.status === 200) {
            setIsActiveTournament(true);
            setActiveTournament(response.data);
          }
          if (response.status === 204) {
            setIsActiveTournament(false);
          }
        },
        (error) => error
      );
    }
  }, [activeSeason]);

  return (
    isActiveTournament ? 
        (activeSeason && activeTournament && <FullTournamentTable season={activeSeason} tournament={activeTournament}/>)
      :
        (
          <Box sx={{ flexGrow: 1, textAlign: 'center'}}>
            <Grid container className='mt-3'>
              <Grid item xs={12}>
                <h1>There is no currently active tournament. Please check in again while there is an ongoing event!</h1>
              </Grid>
            </Grid>
          </Box>
        )
    );
}

export default WeeklyPicks;