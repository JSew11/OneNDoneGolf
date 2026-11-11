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
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

import UsersApi from 'src/api/user';
import SeasonUsersApi from 'src/api/seasonUser';
import { register } from 'src/state/token/actions.jsx';

const UserModal = ({ user = null, creating = false, callback = null, seasonId = null }) => {
  const dispatch = useDispatch();

  const [open, setOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const [userId, setUserId] = useState(null);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('venmo');
  
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const paymentMethodOptions = [
    {
      'value': 'venmo',
      'name': 'Venmo'
    },
    {
      'value': 'cash_app',
      'name': 'Cash App'
    },
    {
      'value': 'paypal',
      'name': 'PayPal'
    },
    {
      'value': 'zelle',
      'name': 'Zelle'
    }
  ]
  
  const buttonText = creating ? 'Register Here' : (user !== null ? 'Edit' : 'Profile');
  const dialogTitleText = creating ? 'Register for One N\' Done' : (user !== null ? 'Editing ' + user.username : 'My Profile');

  const handleOpen = () => {
    if (user !== null) {
      setUserId(user.id);
      setUsername(user.username);
      setEmail(user.email);
      setFirstName(user.first_name ?? '');
      setLastName(user.last_name ?? '');
      setPaymentMethod(user.payment_method ?? 'venmo');
    } else if (!creating) {
      UsersApi.me().then(
        (response) => {
          if (response.data) {
            setUserId(response.data.id);
            setUsername(response.data.username);
            setEmail(response.data.email);
            setFirstName(response.data.first_name ?? '');
            setLastName(response.data.last_name ?? '');
            setPaymentMethod(response.data.payment_method ?? 'venmo');
          }
        }
      )
    } else if (creating) {
      setUserId(null);
      setUsername('');
      setEmail('');
      setFirstName('');
      setLastName('');
      setPaymentMethod('venmo');
    }
    setPassword('');
    setConfirmPassword('');

    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    if (callback !== null) {
      callback();
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage('');
    if (creating) {
      dispatch(register({
        username: username,
        email: email,
        first_name: firstName,
        last_name: lastName,
        payment_method: paymentMethod,
        password: password
      })).then((response) => {
        if (response.status === 201) {
          handleClose();
        } else if (response) {
          setErrorMessage(JSON.stringify(error.response.data));
        }
      });
    } else {
      UsersApi.partialUpdate(userId, {
        username: username,
        email: email,
        first_name: firstName,
        last_name: lastName,
        payment_method: paymentMethod
      }).then((response) => {
        if (response.status === 200) {
          handleClose();
        }
      }).catch((error) => {
        setErrorMessage(JSON.stringify(error.response.data));
      })
    }
  };

  const handleActivateUser = async () => {
    SeasonUsersApi.create(seasonId, user.id)
      .then((response) => {
        if (response.status === 201) {
          handleClose();
        }
      }).catch((error) => {
        setErrorMessage(JSON.stringify(error.response.data));
      })
  }

  const passwordValidation = () => (
    password != '' && password != confirmPassword
  );

  const confirmPasswordValidation = () => (
    confirmPassword != '' && password != confirmPassword
  );

  return (
    <div>
      <Button
        fullWidth={user !== null}
        variant={(creating || user !== null) ? 'contained' : 'text'}
        sx={{
          fontSize: (!creating && user === null) && '1em',
          color: (!creating && user === null) && 'black'
        }}
        onClick={handleOpen}
      >{buttonText}</Button>
      <Dialog
        open={open}
        onClose={handleClose}
        fullWidth
        maxWidth='sm'
      >
        <DialogTitle>
          {dialogTitleText}
          { user && seasonId &&
            <div className='float-end'>
              <Button
                variant='contained'
                disabled={user.active}
                onClick={() => handleActivateUser()}
              >{user.active ? 'User is Active' : 'Add User to Active Season'}</Button>
            </div>
          }
        </DialogTitle>
        <DialogContent>
          <form onSubmit={handleSubmit} id='user-form'>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='username'>Username</InputLabel>
              <OutlinedInput
                id='username'
                label='Username'
                type='text'
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </FormControl>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='email'>Email</InputLabel>
              <OutlinedInput
                id='email'
                label='Email'
                type='email'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </FormControl>
            <FormControl fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='first-name'>First Name</InputLabel>
              <OutlinedInput
                id='first-name'
                label='First Name'
                type='text'
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
            </FormControl>
            <FormControl fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='last-name'>Last Name</InputLabel>
              <OutlinedInput
                id='last-name'
                label='Last Name'
                type='text'
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
              />
            </FormControl>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='payment-method'>Payment Method</InputLabel>
              <Select
                id='payment-method'
                label='Payment Method'
                value={paymentMethod}
                onChange={(e) => setPaymentMethod(e.target.value)}
              >
                {
                  paymentMethodOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>{option.name}</MenuItem>
                  ))
                }
              </Select>
            </FormControl>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='password'>Password</InputLabel>
              <OutlinedInput
                id='password'
                label='Password'
                type={showPassword ? 'text' : 'password'}
                value={password}
                error={passwordValidation()}
                onChange={(e) => setPassword(e.target.value)}
                endAdornment={
                  <InputAdornment position='end'>
                    <IconButton
                      aria-label='toggle password visibility'
                      onClick={() => setShowPassword((show) => !show)}
                      onMouseDown={(event) => {event.preventDefault()}}
                      edge='end'
                    >
                      { showPassword ? <VisibilityOff /> : <Visibility /> }
                    </IconButton>
                  </InputAdornment>
                }
              />
            </FormControl>
            <FormControl required fullWidth variant='outlined' className='my-2'>
              <InputLabel htmlFor='confirm-password'>Confirm Password</InputLabel>
              <OutlinedInput
                id='confirm-password'
                label='Confirm Password'
                type={showConfirmPassword ? 'text' : 'password'}
                value={confirmPassword}
                error={confirmPasswordValidation()}
                onChange={(e) => setConfirmPassword(e.target.value)}
                endAdornment={
                  <InputAdornment position='end'>
                    <IconButton
                      aria-label='toggle password visibility'
                      onClick={() => setShowConfirmPassword((show) => !show)}
                      onMouseDown={(event) => {event.preventDefault()}}
                      edge='end'
                    >
                      { showConfirmPassword ? <VisibilityOff /> : <Visibility /> }
                    </IconButton>
                  </InputAdornment>
                }
              />
            </FormControl>
          </form>
        </DialogContent>
        <DialogContentText className='text-center text-danger'>
          {errorMessage}
        </DialogContentText>
        <DialogActions>
          <Button variant='contained' color='secondary' onClick={handleClose}>Cancel</Button>
          <Button variant='contained' color='primary' type='submit' form='user-form'>{creating ? 'Register' : 'Save Changes'}</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default UserModal;