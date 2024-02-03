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

import TournamentSeasonsApi from 'src/api/tournamentSeason';
import PicksApi from 'src/api/pick';

const PickModal = ({ seasonId, tournamentId }) => {
  const [open, setOpen] = useState(false);
  const [availableGolfers, setAvailableGolfers] = useState([]);
  const [selectedGolferId, setSelectedGolferId] = useState('');

  const handleOpen = () => {
    TournamentSeasonsApi.availableGolfers(seasonId, tournamentId).then(
      (response) => setAvailableGolfers(response.data)
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
    PicksApi.create(seasonId, tournamentId, selectedGolferId).then(
      (response) => console.log(response)
    );
  }

  return (
    <>
      <Button
        fullWidth
        variant='contained'
        color='secondary'
        onClick={handleOpen}
        sx={{
          fontSize: '1.5em'
        }}
      >
        Make Your Pick
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
        <DialogTitle>Make your Pick</DialogTitle>
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
                return <MenuItem key={index} value={golfer.id}>{golfer.first_name} {golfer.last_name}</MenuItem>
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