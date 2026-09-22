import { useState } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';

import { UserDropdownItem } from 'src/pages/header';
import SeasonsApi from 'src/api/season';

const NewSeasonModal = () => {
  const [open, setOpen] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const [name, setName] = useState('');
  const [alias, setAlias] = useState('');
  const [year, setYear] = useState(new Date().getFullYear());

  const handleOpen = () => {
    setSubmitted(false);
    setErrorMessage('');
    setName('');
    setAlias('');
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage('');
    SeasonsApi.create(name, alias, year)
      .then((response) => {
        if (response.status === 200) {
          setSubmitted(true);
        }
      })
      .catch((error) => {
        setErrorMessage(JSON.stringify(error.response.data));
      });
  }

  return (
    <div>
      <UserDropdownItem onClick={handleOpen}>New Season</UserDropdownItem>
      <Dialog
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
        <DialogTitle>Start a New Season</DialogTitle>
        <DialogContent>
          {!submitted ? <div>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='name'>Name</InputLabel>
              <OutlinedInput
                id='name'
                label='Name'
                type='text'
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </FormControl>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='alias'>Alias</InputLabel>
              <OutlinedInput
                id='alias'
                label='alias'
                type='text'
                value={alias}
                onChange={(e) => setAlias(e.target.value)}
              />
            </FormControl>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='year'>Year</InputLabel>
              <OutlinedInput
                id='year'
                label='year'
                type='number'
                value={year}
                onChange={(e) => setYear(e.target.value)}
              />
            </FormControl>
          </div> : 'New Season Created'}
        </DialogContent>
        <DialogContentText className='text-center text-danger'>
          {errorMessage}
        </DialogContentText>
        <DialogActions>
          <Button variant='contained' color='secondary' onClick={handleClose}>{submitted ? 'Exit': 'Cancel'}</Button>
          { !submitted && <Button variant='contained' color='primary' type='submit'>Create</Button> }
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default NewSeasonModal;