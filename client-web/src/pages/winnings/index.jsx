import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import WinningsTable from 'src/assets/components/winningsTable.jsx';

const Winnings = () => {
  return (
    <Box sx={{ flexGrow: 1, textAlign: 'center'}}>
      <Grid container className='mt-3 px-2'>
        <Grid item xs={12}>
          <WinningsTable />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Winnings;