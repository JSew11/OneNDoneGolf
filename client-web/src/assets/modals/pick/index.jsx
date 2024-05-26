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
  const [field, setField] = useState([]);
  const [currentPickPrimarySelectionGolferId, setCurrentPickPrimarySelectionGolferId] = useState('');
  const [primarySelectionGolferId, setPrimarySelectionGolferId] = useState('');
  const [currentPickBackupSelectionGolferId, setCurrentPickBackupSelectionGolferId] = useState('');
  const [backupSelectionGolferId, setBackupSelectionGolferId] = useState('');

  const handleOpen = () => {
    TournamentSeasonsApi.field(season.id, tournament.id).then(
      (response) => {
        setField(response.data);

        if (pick) {
          setCurrentPickPrimarySelectionGolferId(pick['primary_selection']);
          setPrimarySelectionGolferId(pick['primary_selection']);
          setCurrentPickBackupSelectionGolferId(pick['backup_selection']);
          setBackupSelectionGolferId(pick['backup_selection']);
        }
      }
    );

    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handlePrimarySelectionChange = (event) => {
    setPrimarySelectionGolferId(event.target.value);
  };

  const handleBackupSelectionChange = (event) => {
    setBackupSelectionGolferId(event.target.value);
  };

  const handleClear = () => {
    setPrimarySelectionGolferId('');
    setBackupSelectionGolferId('');
  }

  const handleSubmit = () => {
    if (pick) {
      PicksApi.changeGolfer(pick.id, primarySelectionGolferId, backupSelectionGolferId)
    } else {
      PicksApi.create(season.id, tournament.id, primarySelectionGolferId, backupSelectionGolferId);
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
        <DialogTitle>Make your Pick for the {tournament.name}</DialogTitle>
        <DialogContent className='py-0'>
          <FormControl required fullWidth variant='outlined' className='my-2'>
            <InputLabel htmlFor='primary-golfer-select'>Golfer</InputLabel>
            <Select
              id='primary-golfer-select'
              value={primarySelectionGolferId}
              label='Golfer'
              onChange={handlePrimarySelectionChange}
              required
            >
              {field.map((golfer, index) => {
                return <MenuItem 
                          key={index}
                          value={golfer.id}
                          disabled={(golfer.already_picked && currentPickPrimarySelectionGolferId !== golfer.id) || (golfer.id === backupSelectionGolferId)}
                        >
                          <Box sx={{flexGrow: 1}}>
                            <Grid container>
                              <Grid item xs={11} alignItems='self-start'>{golfer.first_name} {golfer.last_name}</Grid>
                              <Grid item xs={1} alignItems='self-end'>{(golfer.id !== currentPickPrimarySelectionGolferId && golfer.tournament_picked_in) ? golfer.tournament_picked_in : ''}</Grid>
                            </Grid>
                          </Box>
                        </MenuItem>
              })}
            </Select>
          </FormControl>
          <FormControl required fullWidth variant='outlined' className='my-2'>
            <InputLabel htmlFor='backup-golfer-select'>Backup Golfer</InputLabel>
            <Select
              id='backup-golfer-select'
              value={backupSelectionGolferId}
              label='Backup Golfer'
              onChange={handleBackupSelectionChange}
              required
            >
              {field.map((golfer, index) => {
                return <MenuItem 
                          key={index}
                          value={golfer.id}
                          disabled={(golfer.already_picked && currentPickBackupSelectionGolferId !== golfer.id) || (golfer.id === primarySelectionGolferId)}
                        >
                          <Box sx={{flexGrow: 1}}>
                            <Grid container>
                              <Grid item xs={11} alignItems='self-start'>{golfer.first_name} {golfer.last_name}</Grid>
                              <Grid item xs={1} alignItems='self-end'>{(golfer.id !== currentPickPrimarySelectionGolferId && golfer.tournament_picked_in) ? golfer.tournament_picked_in : ''}</Grid>
                            </Grid>
                          </Box>
                        </MenuItem>
              })}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions className='px-4 mb-2'>
          <Button
            variant='contained'
            color='secondary'
            onClick={handleClear}
          >
            Clear
          </Button>
          <div style={{flex: '1 0 0'}} />
          <Button
            variant='contained'
            color='error'
            onClick={handleClose}
          >
            Cancel
          </Button>
          <Button
            variant='contained'
            color='primary'
            type='submit'
            disabled={(primarySelectionGolferId === '' || backupSelectionGolferId === '') || (pick && (currentPickPrimarySelectionGolferId === primarySelectionGolferId || currentPickBackupSelectionGolferId === backupSelectionGolferId))}
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default PickModal;