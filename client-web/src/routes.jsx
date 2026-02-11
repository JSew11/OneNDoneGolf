import React from 'react';
import { Route, Routes as Switch } from 'react-router-dom';

import Header from 'src/pages/header/index.jsx';
import Dashboard from 'src/pages/dashboard/index.jsx';
import Error404 from 'src/pages/error404/index.jsx';
import WeeklyPicks from 'src/pages/weeklyPicks/index.jsx';
import ParticipantPicks from 'src/pages/participantPicks/index.jsx';
import Winnings from 'src/pages/winnings/index.jsx';

const Routes = () => (
  <Switch>
    <Route Component={Header}>
      <Route path='/' Component={Dashboard} />
      <Route path='/tournament-standings' Component={WeeklyPicks}/>
      <Route path='/winnings' Component={Winnings}/>
      <Route path='/participant-picks' Component={ParticipantPicks}/>
    </Route>
    <Route path='*' Component={Error404} />
  </Switch>
);

export default Routes;