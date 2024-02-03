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

import SeasonsApi from 'src/api/season';

const PickModal = ({ seasonId, tournamentId=null }) => {
  const [open, setOpen] = useState(false);
  const [selectedGolferId, setSelectedGolferId] = useState(0);

  const handleOpen = () => {
    if (!tournamentId) {
      SeasonsApi.nextTournament(seasonId).then(
        (response) => console.log(response)
      );
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleGolferSelectChange = (event) => {
    setSelectedGolferId(event.target.value);
  };

  const handleSubmit = () => {
    console.log('Need to write this still!');
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
              {/* TODO: loop thru available golfers and show menu items here */}
              <MenuItem value={0}>NEED TO DO THIS</MenuItem>
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