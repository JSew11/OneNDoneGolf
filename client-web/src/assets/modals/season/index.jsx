import { useState } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';

import SeasonsApi from 'src/api/season';

const SeasonModal = ({ season, callback }) => {
  const [open, setOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const [name, setName] = useState('');
  const [alias, setAlias] = useState('');
  const [year, setYear] = useState(dayjs().year());
  const [registrationCutoff, setRegistrationCutoff] = useState(dayjs().endOf('year'));
  const [completed, setCompleted] = useState(false);

  const handleOpen = () => {
    setErrorMessage('');
    setName(season?.name ?? '');
    setAlias(season?.alias ?? '');
    setYear(season?.year ?? year);
    if (season) {
      setRegistrationCutoff(season.registration_cutoff ? dayjs(season.registration_cutoff) : null)
    } else {
      setRegistrationCutoff(dayjs().endOf('year'));
    }
    setCompleted(season?.completed ?? false);
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
    if (callback) {
      callback(true);
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage('');
    if (season) { // edit the existing season provided
      SeasonsApi.partialUpdate(season.id, {
          name: name,
          alias: alias,
          registration_cutoff: registrationCutoff,
          completed: completed
        })
        .then((response) => {
          if (response.status === 200) {
            handleClose();
          }
        })
        .catch((error) => {
          setErrorMessage(JSON.stringify(error.response.data));
        })
    } else { // no season object provided, create a new season
      SeasonsApi.create(name, alias, year, registrationCutoff.format('YYYY-MM-DD'))
        .then((response) => {
          if (response.status === 201) {
            handleClose();
          }
        })
        .catch((error) => {
          setErrorMessage(JSON.stringify(error.response.data));
        });
    }
  }

  return (
    <div>
      <Button
        fullWidth={!season}
        variant='contained'
        size={season ? 'small': 'large'}
        color={season ? 'primary' : 'secondary'}
        onClick={handleOpen}
      >{season ? 'Edit' : 'New Season'}</Button>
      <Dialog
        maxWidth='xs'
        open={open}
        onClose={handleClose}
      >
        <DialogTitle>{season ? 'Editing ' + season.name : 'Start a New Season'}</DialogTitle>
        <DialogContent>
          <form onSubmit={handleSubmit} id='season-form'>
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
                disabled={!!season}
              />
            </FormControl>
            <FormControl fullWidth className='my-2'>
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DatePicker
                  label='Registration Cutoff'
                  value={registrationCutoff}
                  onChange={(newValue) => setRegistrationCutoff(newValue)}
                />
              </LocalizationProvider>
            </FormControl>
            { season && 
              <FormControlLabel 
                control={<Checkbox 
                  checked={completed}
                  onChange={() => setCompleted(!completed)}
                  name='completed'
                />}
                label='Completed'
              />
            }
          </form>
        </DialogContent>
        <DialogContentText className='text-center text-danger'>
          {errorMessage}
        </DialogContentText>
        <DialogActions>
          <Button variant='contained' color='secondary' onClick={handleClose}>Cancel</Button>
          <Button variant='contained' color='primary' type='submit' form='season-form'>{season ? 'Save' : 'Create'}</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default SeasonModal;