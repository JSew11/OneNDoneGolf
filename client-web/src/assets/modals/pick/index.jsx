import { useState } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

import TournamentSeasonsApi from 'src/api/tournamentSeason';
import PicksApi from 'src/api/pick';

const PickModal = ({ season, tournament, pick }) => {
  const [open, setOpen] = useState(false);
  const [availableGolfers, setAvailableGolfers] = useState([]);
  const [currentPickGolferId, setCurrentPickGolferId] = useState('');
  const [selectedGolferId, setSelectedGolferId] = useState('');

  const handleOpen = () => {
    TournamentSeasonsApi.availableGolfers(season.id, tournament.id).then(
      (response) => {
        setAvailableGolfers(response.data);

        if (pick) {
          setCurrentPickGolferId(pick['golfer']);
          setSelectedGolferId(pick['golfer']);
        }
      }
    );

    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleGolferSelectChange = (event) => {
    setSelectedGolferId(event.target.value);
  };

  const handleSubmit = () => {
    if (pick) {
      PicksApi.changeGolfer(pick.id, selectedGolferId)
    } else {
      PicksApi.create(season.id, tournament.id, selectedGolferId);
    }
  }

  return (
    <>
      <Button
        fullWidth
        variant='contained'
        onClick={handleOpen}
        sx={{
          backgroundColor: 'royalblue',
          fontSize: '1.5em',
          ':hover': {
            backgroundColor: '#2d499d'
          },
        }}
      >
        { pick ? 
          'Change Your Pick' :
          'Make Your Pick'
        }
      </Button>
      <Dialog
        fullWidth
        open={open}
        onClose={handleClose}
        PaperProps={{
          component: 'form',
          onSubmit: handleSubmit,
          sx: {
            maxWidth: '50%'
          }
        }}
      >
        <DialogTitle>Pick your Golfer for the {tournament.name}</DialogTitle>
        <DialogContent>
          <FormControl required fullWidth variant='outlined' className='my-2'>
            <InputLabel htmlFor='golfer-select'>Golfer</InputLabel>
            <Select
              id='golfer-select'
              value={selectedGolferId}
              label='Golfer'
              onChange={handleGolferSelectChange}
            >
              {availableGolfers.map((golfer, index) => {
                return <MenuItem 
                          key={index}
                          value={golfer.id}
                          disabled={golfer.already_picked && currentPickGolferId !== golfer.id}
                        >
                          <Box sx={{flexGrow: 1}}>
                            <Grid container>
                              <Grid item xs={11} alignItems='self-start'>{golfer.first_name} {golfer.last_name}</Grid>
                              <Grid item xs={1} alignItems='self-end'>{(golfer.id !== currentPickGolferId && golfer.tournament_picked_in) ? golfer.tournament_picked_in : ''}</Grid>
                            </Grid>
                          </Box>
                        </MenuItem>
              })}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button variant='contained' color='error' onClick={handleClose}>Cancel</Button>
          <Button variant='contained' color='primary' type='submit'>Submit</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default PickModal;