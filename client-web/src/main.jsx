import React from 'react'
import ReactDOM from 'react-dom/client'
import axios from 'axios'
import { CookiesProvider } from 'react-cookie'
import { Provider } from 'react-redux'
import { CssBaseline, ThemeProvider } from '@mui/material'

import App from './app.jsx'
import './index.scss'
import store from 'src/state/store.jsx'
import { appTheme } from 'src/theme.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <CookiesProvider>
      <Provider store={store}>
        <ThemeProvider theme={appTheme}>
          <CssBaseline />
          <App />
        </ThemeProvider>
      </Provider>
    </CookiesProvider>
  </React.StrictMode>,
)
