import React from 'react';
import { Route, Routes as Switch } from 'react-router-dom';

import Header from './pages/header/index.jsx';
import Dashboard from './pages/dashboard/index.jsx';
import Error404 from './pages/error404/index.jsx';

const Routes = () => (
  <Switch>
    <Route Component={Header}>
      <Route path='/' Component={Dashboard} />
    </Route>
    <Route path='*' Component={Error404} />
  </Switch>
);

export default Routes;