import { useState } from 'react';
import { useDispatch } from 'react-redux';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

import { login } from 'src/state/token/actions.jsx';

export default function LoginModal() {
  const [open, setOpen] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const dispatch = useDispatch();

  const handleOpen = () => {
    setUsername('');
    setPassword('');
    setErrorMessage('');
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <div>
      <Button variant='contained' onClick={handleOpen}>Log In</Button>
      <Dialog
        open={open}
        onClose={handleClose}
        PaperProps={{
          component: 'form',
          onSubmit: async (event) => {
            event.preventDefault();
            dispatch(login(username, password)).then(
              (result) => {
                if (result.response && result.response.status !== 200) {
                  setErrorMessage(result.response.data.detail);
                }
              },
            );
          }
        }}
      >
        <DialogTitle>Log In</DialogTitle>
        <DialogContent>
          <FormControl required variant='outlined' fullWidth className='my-2'>
            <InputLabel htmlFor='username'>Username</InputLabel>
            <OutlinedInput
              id='username'
              label='Username'
              type='text'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </FormControl>
          <FormControl required variant='outlined' fullWidth>
            <InputLabel htmlFor='password'>Password</InputLabel>
            <OutlinedInput 
              id='password'
              label='Password'
              type={ showPassword ? 'text' : 'password' }
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              endAdornment={
                <InputAdornment position='end'>
                  <IconButton
                    aria-label='toggle password visibility'
                    onClick={handleClickShowPassword}
                    onMouseDown={handleMouseDownPassword}
                    edge='end'
                  >
                    { showPassword ? <VisibilityOff /> : <Visibility /> }
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>
        </DialogContent>
        <DialogContentText className='text-center text-danger'>
          {errorMessage}
        </DialogContentText>
        <DialogActions>
          <Button variant='contained' color='secondary' onClick={handleClose}>Cancel</Button>
          <Button variant='contained' color='primary' type='submit'>Log In</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}