import { useState } from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import Dialog from '@mui/material/Dialog';

function ButtonConfirm(props) {
  const { onClick, buttonText, title, message, ...other } = props;
  const [open, setOpen] = useState(false);

  const handleConfirm = () => {
    onClick();
    handleClose();
  };

  const handleOpen = () => {
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  return (
    <div>
      <Button
        variant={other.buttonVariant ?? 'contained'}
        color={other.buttonColor ?? 'primary'}
        sx={other.buttonSx}
        onClick={handleOpen}
      >{buttonText}</Button>
      <Dialog open={open}>
        <DialogTitle className='mx-2 px-2'>{title}</DialogTitle>
        <DialogContentText className='m-2 px-2 text-dark'>
          {message}
        </DialogContentText>
        <DialogActions>
          <Button autoFocus onClick={handleClose} color='secondary'>
            Cancel
          </Button>
          <Button onClick={handleConfirm} color={other.buttonColor}>Confirm</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

ButtonConfirm.propTypes = {
  onClick: PropTypes.func.isRequired,
  buttonText: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
};

export default ButtonConfirm;