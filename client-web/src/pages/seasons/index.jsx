import { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

import SeasonsTable from 'src/pages/seasons/seasonsTable';
import SeasonModal from 'src/assets/modals/season';
import SeasonsApi from 'src/api/season';

const Seasons = () => {
  const [activeSeason, setActiveSeason] = useState(null);
  const [incompleteSeasons, setIncompleteSeasons] = useState([]);

  useEffect(() => {
    SeasonsApi.list().then(
      (response) => {
        if (response.data.length > 0) {
          setIncompleteSeasons(response.data.filter((season) => !!!season.completed));
          setActiveSeason(response.data.filter((season) => season.active)[0])
        }
      }
    );
  }, []);

  const handleChange = (event) => {
    SeasonsApi.setActiveSeason(event.target.value.id).then(
      (response) => {
        if (response.status === 200) {
          setActiveSeason(event.target.value);
        }
      }
    );
  }

  return (
    <Box sx={{ flexGrow: 1, textAlign: 'center'}}>
      <Grid container className='my-3 px-2'>
        <Grid size={7}>
          { activeSeason && incompleteSeasons.length > 0 ?
            <FormControl variant='outlined' fullWidth className='px-2'>
                <InputLabel id='active-season-label' className='px-2'>Active Season</InputLabel>
                <Select
                  labelId='active-season-label'
                  id='active-season'
                  value={activeSeason}
                  label='Active Season'
                  onChange={handleChange}
                >
                  {
                    incompleteSeasons.map((season) => (
                      <MenuItem key={season.id} value={season}>
                        {season.name}
                      </MenuItem>
                    ))
                  }
                </Select>
              </FormControl>
            :
              'Loading Table Data'
          }
        </Grid>
        <Grid size={3}></Grid>
        <Grid size={2}><SeasonModal /></Grid>
      </Grid>
      <Grid container className='px-2'>
        <Grid size={12}>
          <SeasonsTable />
        </Grid>
      </Grid>
    </Box>
  );
}

export default Seasons;