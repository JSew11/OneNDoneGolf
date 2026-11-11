import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import UsersTable from 'src/pages/users/usersTable';

const Users = () => {
  return (
    <Box sx={{ flexGrow: 1, textAlign: 'center'}}>
      <Grid container className='my-3 px-2'>
        <Grid size={12}>
          <UsersTable />
        </Grid>
      </Grid>
    </Box>
  )
};

export default Users;