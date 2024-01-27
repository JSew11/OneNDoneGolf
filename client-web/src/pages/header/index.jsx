import { useSelector } from 'react-redux';
import { useNavigate, Outlet } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import { 
  Box,
  Grid,
  Button,
  AppBar,
  Toolbar,
} from '@mui/material';

import LoginModal from 'src/assets/modals/login';

const NavBarLink = styled(Button)(({ theme }) => ({
  color: theme.palette.primary.contrastText,
  backgroundColor: theme.palette.primary.main,
  '&:hover': {
    color: theme.palette.primary.contrastText,
    backgroundColor: theme.palette.primary.dark,
  },
  variant: 'contained',
  disableElevation: true,
  borderRadius: 0,
  margin: 0,
  padding: '8px 10px',
}));

const Header = () => {
  const APP_NAME = import.meta.env.VITE_APP_NAME;

  const navigate = useNavigate();

  const { isLoggedIn } = useSelector(state => state.auth);
  
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container justifyContent='flex-end' alignItems='center' className='p-2'>
          <Grid item xs={8} onClick={() => {navigate('/');}}>
            <h1 className='site-logo'>{APP_NAME}</h1>
          </Grid>
          <Grid item xs={4} className='m-0 p-0 text-end'>
            {
              isLoggedIn ?
              <Button color='primary' variant='outlined'>Profile Placeholder</Button> :
              <LoginModal />
            }
          </Grid>
        </Grid>
        <Grid container>
          <AppBar position='static' color='primary' className='mx-0 px-1' elevation={0}>
            <Toolbar variant='dense' className='m-0 p-0'>
              <NavBarLink href='#'>Link Placeholder</NavBarLink>
            </Toolbar>
          </AppBar>
        </Grid>
      </Box>
      <Outlet />
    </>
  );
}

export default Header;