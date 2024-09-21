import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsApi from 'src/api/season';
import PickModal from 'src/assets/modals/pick';
import QuickStandingsTable from 'src/pages/dashboard/quickStandingsTable';
import GameInformation from 'src/pages/dashboard/gameInformation';

const Dashboard = () => {
  const [activeSeason, setActiveSeason] = useState(null);
  const [nextTournament, setNextTournament] = useState(null);
  const [pick, setPick] = useState(false);
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
      SeasonsApi.nextTournament(activeSeason.id).then(
        (response) => {
          if (response.status === 200) {
            setNextTournament(response.data['tournament']);
            setPick(response.data['user_pick']);
          }
        },
        (error) => error
      );
    }
  }, [activeSeason])

  return (
    <Box sx={{ flexGrow: 1 }}>
      { isLoggedIn && activeSeason && nextTournament && 
        <Grid container justifyContent='center' alignItems='center' className='py-4'>
          <Grid item xs={8}>
            <PickModal season={activeSeason} tournament={nextTournament} pick={pick}/>
          </Grid>
        </Grid>
      }
      <Grid container justifyContent='center' alignItems='center'>
        <Grid item xs={10}>
          { 
            isLoggedIn ?
            <QuickStandingsTable seasonId={activeSeason?.id}/> :
            <GameInformation />
          }
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;