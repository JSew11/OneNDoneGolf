import { useEffect } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import PickModal from 'src/assets/modals/pick';
import QuickStandingsTable from 'src/pages/dashboard/quickStandingsTable';

const Dashboard = () => {
  const { isLoggedIn } = useSelector(state => state.auth);

  useEffect(() => {
    if (isLoggedIn) {
      // TODO: call API to get user-specific dashboard data
    } else {
      // TODO: call API to get generic dashboard data
    }
  }, [isLoggedIn]);

  return (
    isLoggedIn ? <UserDashboard /> : <GenericDashboard />
  );
}

const UserDashboard = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container justifyContent='center' alignItems='center' className='py-4'>
        <Grid item xs={8}>
          <PickModal />
        </Grid>
      </Grid>
      <Grid container justifyContent='center' alignItems='center'>
        <Grid item xs={10}>
          <QuickStandingsTable />
        </Grid>
      </Grid>
    </Box>
  );
};

const GenericDashboard = () => {
  return (
    <h1 className='text-center'>Not Logged In</h1>
  );
};

export default Dashboard;