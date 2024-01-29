import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate, Outlet } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import { styled } from '@mui/material/styles';
import { 
  Box,
  Grid,
  Button,
  AppBar,
  Toolbar,
  Menu,
  MenuItem,
} from '@mui/material';
import KeyboardArrowDown from '@mui/icons-material/KeyboardArrowDown';

import { logout } from 'src/state/token/actions';
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

const UserDropdownItem = styled(MenuItem)(({theme}) => ({
  justifyContent: 'flex-end'
}));

const Header = () => {
  const APP_NAME = import.meta.env.VITE_APP_NAME;

  const [username, setUsername] = useState('');

  const navigate = useNavigate();

  const { isLoggedIn, access } = useSelector(state => state.auth);

  useEffect(() => {
    if (access !== null) {
      setUsername(jwtDecode(access)['username']);
    }
  }, [access]);

  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container justifyContent='flex-end' alignItems='center' className='py-2 px-4'>
          <Grid item xs={8} onClick={() => {navigate('/');}}>
            <h1 className='site-logo'>{APP_NAME}</h1>
          </Grid>
          <Grid item xs={4} className='text-end'>
            {
              isLoggedIn ?
              <UserDropdown userName={username}/> :
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

const UserDropdownMenu = styled((props) => (
  <Menu
    elevation={0}
    anchorOrigin={{
      vertical: 'bottom',
      horizontal: 'right',
    }}
    transformOrigin={{
      vertical: 'top',
      horizontal: 'right',
    }}
    {...props}
  />
))(({ theme }) => ({
  '& .MuiPaper-root': {
    borderRadius: 3,
    marginTop: 0,
    minWidth: 180,
    '& .MuiMenu-list': {
      padding: '4px 0',
    },
  },
}));

const UserDropdown = ({ userName }) => {
  const [userDropdownAnchorEl, setUserDropdownAnchorEl] = useState(null);
  const isUserDropdownOpen = Boolean(userDropdownAnchorEl);

  const navigate = useNavigate();

  const dispatch = useDispatch();

  const openUserDropdown = (event) => {
    setUserDropdownAnchorEl(event.currentTarget);
  };

  const closeUserDropdown = () => {
    setUserDropdownAnchorEl(null);
  };
  
  const logoutUser = () => {
    dispatch(logout());
    closeUserDropdown();
    navigate('/');
  };

  return (
    <>
      <Button
        id='user-dropdown'
        aria-controls={isUserDropdownOpen ? 'user-menu': undefined}
        aria-haspopup='true'
        aria-expanded={isUserDropdownOpen ? 'true': undefined}
        color='secondary'
        disableElevation
        variant='contained'
        onClick={openUserDropdown}
        sx={{ fontSize: '1em' }}
        endIcon={<KeyboardArrowDown />}
      >
        {userName}
      </Button>
      <UserDropdownMenu
        id='user-menu'
        anchorEl={userDropdownAnchorEl}
        open={isUserDropdownOpen}
        onClose={closeUserDropdown}
        MenuListProps={{
          'aria-labelledby': 'user-dropdown'
        }}
      >
        <UserDropdownItem onClick={logoutUser}>Logout</UserDropdownItem>
      </UserDropdownMenu>
    </>
  );
}

export default Header;