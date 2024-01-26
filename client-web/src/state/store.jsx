import { applyMiddleware } from 'redux';
import { configureStore } from '@reduxjs/toolkit';
import { composeWithDevTools } from 'redux-devtools-extension';
import thunk from 'redux-thunk';

import auth from 'src/state/token/reducer';

const middleware = [thunk];

const store = configureStore(
  {
    reducer: {
      auth
    }
  },
  composeWithDevTools(applyMiddleware(...middleware))
);

export default store;