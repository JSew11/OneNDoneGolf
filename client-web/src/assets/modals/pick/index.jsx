import { useState } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';

const PickModal = ({ isLoggedIn }) => {
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
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
        disabled={!isLoggedIn}
        sx={{
          fontSize: '1.5em'
        }}
      >
        { !isLoggedIn && 'Log In to ' } Make Your Pick
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
      >
        <DialogTitle>Make your Pick</DialogTitle>
        <DialogContent>
          Work in Progress
        </DialogContent>
        <DialogActions>
          <Button variant='contained' color='error' onClick={handleClose}>Cancel</Button>
          <Button variant='contained' color='primary' type='submit' onClick={handleSubmit}>Submit</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default PickModal;