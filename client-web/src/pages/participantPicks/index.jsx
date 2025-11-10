import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

const ParticipantPicks = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          TODO - put Participant Picks table here
        </Grid>
      </Grid>
    </Box>
  )
};

export default ParticipantPicks;