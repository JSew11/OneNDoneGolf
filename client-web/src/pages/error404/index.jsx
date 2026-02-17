import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';

const Error404 = () => {
  const APP_NAME = import.meta.env.VITE_APP_NAME;

  const navigate = useNavigate();

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container className='p-2'>
        <Grid item xs={12}><h1 className='text-center'>{APP_NAME}</h1></Grid>
      </Grid>
      <Grid container className='p-2'>
        <Grid item xs={12}><h3 className='text-center'>404: This page could not be found</h3></Grid>
      </Grid>
      <Grid container className='p-2'>
        <Grid item xs={12} className='text-center'><Button onClick={() => {navigate('/');}} disableElevation variant='contained'>Home</Button></Grid>
      </Grid>
    </Box>
  );
};

export default Error404;