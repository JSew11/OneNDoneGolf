import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import {
  Route,
  Routes as Switch,
  Outlet,
  Navigate
} from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

import Header from 'src/pages/header/index.jsx';
import Dashboard from 'src/pages/dashboard/index.jsx';
import Error404 from 'src/pages/error404/index.jsx';
import WeeklyPicks from 'src/pages/weeklyPicks/index.jsx';
import ParticipantPicks from 'src/pages/participantPicks/index.jsx';
import Winnings from 'src/pages/winnings/index.jsx';
import TournamentSchedule from './pages/tournamentSchedule';
import OWGR from './pages/owgr';
import Seasons from './pages/seasons';

const Routes = () => {
  const [isAdminUser, setIsAdminUser] = useState(false);

  const { isLoggedIn, access } = useSelector(state => state.auth);

  useEffect(() => {
    if (access !== null) {
      setIsAdminUser(jwtDecode(access)['isAdmin']);
    }
  }, [access]);

  return (
    <Switch>
      <Route Component={Header}>
        <Route path='/' Component={Dashboard} />
        <Route element={<PrivateRoute isLoggedIn={isLoggedIn} />}>
          <Route path='/tournament-standings' Component={WeeklyPicks}/>
          <Route path='/winnings' Component={Winnings}/>
          <Route path='/participant-picks' Component={ParticipantPicks}/>
          <Route path='/schedule' Component={TournamentSchedule} />
          <Route path='/owgr' Component={OWGR} />
          <Route element={<AdminRoute isAdmin={isAdminUser}/>}>
            <Route path='/seasons' Component={Seasons} />
          </Route>
        </Route>
      </Route>
      <Route path='*' Component={Error404} />
    </Switch>
  )
};

const PrivateRoute = ({ isLoggedIn }) => {
  return isLoggedIn ? <Outlet /> : <Navigate to='/page-not-found' />;
}

const AdminRoute = ({ isAdmin }) => {
  return isAdmin ? <Outlet /> : <Navigate to='/page-not-found' />;
};

export default Routes;