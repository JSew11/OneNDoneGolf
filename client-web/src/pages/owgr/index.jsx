import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import { jwtDecode } from 'jwt-decode';

import SeasonsApi from 'src/api/season';
import OWGRTable from 'src/pages/owgr/owgrTable';

const OWGR = () => {

  const [activeSeason, setActiveSeason] = useState(null);
  const [isAdminUser, setIsAdminUser] = useState(false);
  
  const { isLoggedIn, access } = useSelector(state => state.auth);

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
    if (access !== null) {
      setIsAdminUser(jwtDecode(access)['isAdmin']);
    }
  }, [access]);

  return (
    <Box sx={{ flexGrow: 1, textAlign: 'center'}}>
      <Grid container className='mt-3 px-2'>
        <Grid size={12}>
          <OWGRTable seasonId={activeSeason?.id} isAdminUser={isAdminUser} />
        </Grid>
      </Grid>
    </Box>
  );
}

export default OWGR;