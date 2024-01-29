import { createTheme } from '@mui/material';

const PRIMARY_COLOR_LIGHT = '#9bba8e';
const PRIMARY_COLOR_MAIN = '#38761d';
const PRIMARY_COLOR_DARK = '#1c3b0e';
const PRIMARY_COLOR_CONTRAST = '#ffffff';

const SECONDARY_COLOR_LIGHT = '#cbe3c2';
const SECONDARY_COLOR_MAIN = '#b6d7a8';
const SECONDARY_COLOR_DARK = '#7f9675';
const SECONDARY_COLOR_CONTRAST = '#000000';

const SITE_BACKGROUND_COLOR = '#f0f0f0';
const DISABLED_CONTRAST_COLOR = '#999999';

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
    background: {
      default: SITE_BACKGROUND_COLOR,
      paper: '#ffffff'
    },
    primary: {
      light: PRIMARY_COLOR_LIGHT,
      main: PRIMARY_COLOR_MAIN,
      dark: PRIMARY_COLOR_DARK,
      contrastText: PRIMARY_COLOR_CONTRAST,
    },
    secondary: {
      light: SECONDARY_COLOR_LIGHT,
      main: SECONDARY_COLOR_MAIN,
      dark: SECONDARY_COLOR_DARK,
      contrastText: SECONDARY_COLOR_CONTRAST,
    },
  },
  components: {
    MuiButton: {
      defaultProps: {
        disableRipple: true,
      },
      styleOverrides: {
        root: ({ ownerState }) => ({
          ...(ownerState.variant === 'contained' && (
            (ownerState.color === 'primary' && {
              '&:disabled': {
                backgroundColor: PRIMARY_COLOR_LIGHT,
                color: DISABLED_CONTRAST_COLOR,
              },
            }) || 
            (ownerState.color === 'secondary' && {
              '&:disabled': {
                backgroundColor: SECONDARY_COLOR_LIGHT,
                color: DISABLED_CONTRAST_COLOR,
              }
            })
          )),
        }),
      },
    },
  },
});