import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate, Outlet, Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import { styled } from '@mui/material/styles';
import { 
  Box,
  Grid,
  Button,
  Menu,
  MenuItem,
  Tabs,
  Tab,
  AppBar,
} from '@mui/material';
import KeyboardArrowDown from '@mui/icons-material/KeyboardArrowDown';

import { logout } from 'src/state/token/actions';
import LoginModal from 'src/assets/modals/login';

const UserDropdownItem = styled(MenuItem)(({theme}) => ({
  justifyContent: 'flex-end'
}));

const Header = () => {
  const APP_NAME = import.meta.env.VITE_APP_NAME;

  const [username, setUsername] = useState('');
  const [tabs, setTabs] = useState([]);

  const navigate = useNavigate();

  const { isLoggedIn, access } = useSelector(state => state.auth);

  useEffect(() => {
    if (access !== null) {
      setUsername(jwtDecode(access)['username']);
    }
  }, [access]);

  useEffect(() => {
    const availableTabs = [{'key': 0, 'label': 'Home Page', 'link': '/'}];

    if (isLoggedIn) {
      availableTabs.push(
        {'key': 1, 'label': 'Full Standings', 'link': '/full-standings'},
        {'key': 2, 'label': 'Weekly Picks', 'link': '/weekly-picks'},
        {'key': 3, 'label': 'Winnings', 'link': '/winnings'},
        {'key': 4, 'label': 'OWGR', 'link': '/owgr'},
        {'key': 5, 'label': 'Participant Picks', 'link': '/participant-picks'},
        {'key': 6, 'label': 'PGA Tour Schedule', 'link': '/pga-tour-schedule'}
      );
    }

    setTabs(availableTabs);
  }, [isLoggedIn]);

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
              <UserDropdown username={username}/> :
              <LoginModal />
            }
          </Grid>
        </Grid>
      </Box>
      <NavTabs tabs={tabs}/>
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

const UserDropdown = ({ username }) => {
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
        {username}
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

function LinkTab(props) {
  return (
    <Tab
      component={Link}
      aria-current={props.selected && 'page'}
      {...props}
    />
  );
}

LinkTab.propTypes = {
  selected: PropTypes.bool,
};

const samePageLinkNavigation = (event) => {
  if (
    event.defaultPrevented ||
    event.button !== 0 || // ignore everything but left-click
    event.metaKey ||
    event.ctrlKey ||
    event.altKey ||
    event.shiftKey
  ) {
    return false;
  }
  return true;
}

const NavTabs = ({ tabs }) => {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    if (
      event.type !== 'click' ||
      (event.type === 'click' && samePageLinkNavigation(event))
    ) {
      setValue(newValue);
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      <AppBar position='static'>
        <Tabs
          key='header-nav'
          value={value}
          onChange={handleChange}
          indicatorColor='secondary'
          textColor='inherit'
          aria-label='one-n-done-golf-nav'
          role='navigation'
        >
          {
            tabs.map((tab) => (
              <LinkTab key={tab.key} label={tab.label} to={tab.link} />
            ))
          }
        </Tabs>
      </AppBar>
    </Box>
  );
}

export default Header;