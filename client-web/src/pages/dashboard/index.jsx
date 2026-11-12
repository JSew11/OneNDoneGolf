import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsApi from 'src/api/season';
import PickModal from 'src/assets/modals/pick';
import PickemStandingsTable from 'src/pages/dashboard/pickemStandingsTable';
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
    if (activeSeason !== null && activeSeason['user_active'] === 'true') {
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
        <Grid container className='pt-4 justify-content-center'>
          <Grid size={8}>
            <PickModal season={activeSeason} tournament={nextTournament} pick={pick} setPick={setPick} />
          </Grid>
        </Grid>
      }
      <Grid container className='pt-4 justify-content-center'>
        <Grid size={10}>
          { 
            isLoggedIn ?
            <PickemStandingsTable seasonId={activeSeason?.id}/> :
            <GameInformation />
          }
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;