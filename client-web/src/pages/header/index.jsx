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
  ListSubheader,
  Divider,
} from '@mui/material';
import KeyboardArrowDown from '@mui/icons-material/KeyboardArrowDown';

import { logout } from 'src/state/token/actions';
import LoginModal from 'src/assets/modals/login';

const Header = () => {
  const APP_NAME = import.meta.env.VITE_APP_NAME;

  const [username, setUsername] = useState('');
  const [isAdminUser, setIsAdminUser] = useState(false);
  const [tabs, setTabs] = useState([]);

  const navigate = useNavigate();

  const { isLoggedIn, access } = useSelector(state => state.auth);

  useEffect(() => {
    if (access !== null) {
      setUsername(jwtDecode(access)['username']);
      setIsAdminUser(jwtDecode(access)['isAdmin']);
    }
  }, [access]);

  useEffect(() => {
    const availableTabs = [{'key': 0, 'label': 'Pickem Home', 'link': '/'}];

    if (isLoggedIn) {
      availableTabs.push(
        {'key': 1, 'label': 'Tournament Standings', 'link': '/tournament-standings'},
        {'key': 2, 'label': 'Winnings', 'link': '/winnings'},
        {'key': 3, 'label': 'OWGR', 'link': '/owgr'},
        {'key': 4, 'label': 'Participant Picks', 'link': '/participant-picks'},
        {'key': 5, 'label': 'PGA Tour Schedule', 'link': '/schedule'}
      );
    }

    setTabs(availableTabs);
  }, [isLoggedIn]);

  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container className='py-2 px-4'>
          <Grid size={8} onClick={() => {navigate('/');}}>
            <h1 className='site-logo'>{APP_NAME}</h1>
          </Grid>
          <Grid size={4} className='text-end'>
            {
              isLoggedIn ?
              <UserDropdown username={username} isAdminUser={isAdminUser}/> :
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

export const UserDropdownItem = styled(MenuItem)(({theme}) => ({
  justifyContent: 'flex-end'
}));

const UserDropdownListHeader = styled(ListSubheader)({
  backgroundImage: 'var(--Paper-overlay)',
});

const UserDropdown = ({ username, isAdminUser }) => {
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
        onClick={closeUserDropdown}
        slotProps={{
          list: {
            'aria-labelledby': 'user-dropdown'
          },
        }}
      >
        { isAdminUser && (
          <div>
            <UserDropdownListHeader>Admin</UserDropdownListHeader>
            <UserDropdownItem component={Link} to="/users">Users</UserDropdownItem>
            <UserDropdownItem component={Link} to="/seasons">Seasons</UserDropdownItem>
            <Divider sx={{ my: 0.5 }} />
          </div>
        )}
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

const NavTabs = ({ tabs }) => {
  const [linkKeyMap, setLinkKeyMap] = useState({});
  
  const { pathname } = window.location;

  useEffect(() => {
    const tempMap = {};
    tabs.forEach(tab => {
      tempMap[tab.link] = tab.key;
    });
    setLinkKeyMap(tempMap);
  }, [tabs])

  return (
    <Box sx={{ width: '100%' }}>
      <AppBar position='static'>
        <Tabs
          key='header-nav'
          value={linkKeyMap[pathname] ?? false}
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