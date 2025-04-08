import { useEffect, useState } from 'react';
import { useTheme } from '@mui/material';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import FormControl from '@mui/material/FormControl';
import { InputLabel, Select, MenuItem } from '@mui/material';

import SeasonsApi from 'src/api/season';
import PickedGolfersLeaderboard from 'src/assets/components/pickedGolfersLeaderboard';
import FullTournamentLeaderboard from 'src/assets/components/fullTournamentLeaderboard';

const WeeklyPicks = () => {
  const theme = useTheme();

  const [activeSeason, setActiveSeason] = useState(null);
  const [activeTournament, setActiveTournament] = useState(null);
  const [selectedTable, setSelectedTable] = useState('full-tournament');
  
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

  // TODO - get the active tournament and pass id to tables, display name above table

  const handleChange = (event) => {
    setSelectedTable(event.target.value);
  }

  return (
    <Box sx={{ flexGrow: 1, textAlign: 'center' }}>
      <Grid container className='mt-3'>
        <Grid item xs={12} className='playfair-display'
              sx={{color: theme.palette.primary.dark}}>
          <h2>{
            activeTournament ? 
              activeTournament.tournament.name
            :
              'Loading Active Tournament'
          }</h2>
        </Grid>
      </Grid>
      <Grid container>
        <Grid item xs={12}>
          <FormControl fullWidth size='small' className='mt-3 px-2'>
            <Select
              labelId='weekly-picks-table-select-label'
              id='weekly-picks-table-select'
              value={selectedTable}
              onChange={handleChange}
              sx={{
                backgroundColor: theme.palette.primary.main,
                color: theme.palette.primary.contrastText,
                '.MuiOutlinedInput-notchedOutline': {
                  borderColor: theme.palette.primary.light,
                },
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                  borderColor: theme.palette.primary.main,
                },
                '&:hover .MuiOutlinedInput-notchedOutline': {
                  borderColor: theme.palette.primary.main,
                },
                '.MuiSvgIcon-root ': {
                  fill: theme.palette.primary.contrastText,
                }
              }}
            >
              <MenuItem key='full-tournament-option' value='full-tournament'>
                Full Leaderboard
              </MenuItem>
              <MenuItem key='picked-golfers-option' value='picked-golfers'>
                Picked Golfers Leaderboard
              </MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>
      <Grid container className='px-2'>
        <Grid item xs={12}>
          {selectedTable === 'picked-golfers' && <PickedGolfersLeaderboard seasonId={activeSeason?.id} />}
          {selectedTable === 'full-tournament' && <FullTournamentLeaderboard seasonId={activeSeason?.id} />}
        </Grid>
      </Grid>
    </Box>
  );
}

export default WeeklyPicks;