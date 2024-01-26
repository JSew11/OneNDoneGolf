import { createTheme } from '@mui/material';

const PRIMARY_COLOR_LIGHT = '#9bba8e';
const PRIMARY_COLOR_MAIN = '#38761d';
const PRIMARY_COLOR_DARK = '#1c3b0e';

const SECONDARY_COLOR_LIGHT = '#cbe3c2';
const SECONDARY_COLOR_MAIN = '#b6d7a8';
const SECONDARY_COLOR_DARK = '#7f9675';

export const appTheme = createTheme({
  typography: {
    fontFamily: [
      'Arial',
    ].join('.'),
    button: {
      textTransform: 'none',
    },
  },
  palette: {
    primary: {
      light: PRIMARY_COLOR_LIGHT,
      main: PRIMARY_COLOR_MAIN,
      dark: PRIMARY_COLOR_DARK,
      contrastText: '#ffffff',
    },
    secondary: {
      light: SECONDARY_COLOR_LIGHT,
      main: SECONDARY_COLOR_MAIN,
      dark: SECONDARY_COLOR_DARK,
      contrastText: '#000000',
    },
  },
  components: {
    MuiButtonBase: {
      defaultProps: {
        disableRipple: true,
      },
    },
  },
});