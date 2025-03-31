import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import SeasonsApi from 'src/api/season';
import PickedGolfersLeaderboard from 'src/assets/components/pickedGolfersLeaderboard';

const WeeklyPicks = () => {
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
      <Grid container spacing={1} className='px-2'>
        <Grid item xs={5}>
          
        </Grid>
      </Grid>
    </Box>
  );
}

export default WeeklyPicks;