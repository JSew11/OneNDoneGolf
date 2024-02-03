import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsApi from 'src/api/season';
import PickModal from 'src/assets/modals/pick';
import QuickStandingsTable from 'src/pages/dashboard/quickStandingsTable';
import GameInformation from 'src/pages/dashboard/gameInformation';

const Dashboard = () => {
  const [activeSeason, setActiveSeason] = useState({});
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
    } else {
      // TODO: call API to get generic dashboard data
    }
  }, [isLoggedIn]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      { isLoggedIn && 
        <Grid container justifyContent='center' alignItems='center' className='py-4'>
          <Grid item xs={8}>
            <PickModal seasonId={activeSeason.id}/>
          </Grid>
        </Grid>
      }
      <Grid container justifyContent='center' alignItems='center'>
        <Grid item xs={10}>
          { 
            isLoggedIn ?
            <QuickStandingsTable /> :
            <GameInformation />
          }
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;