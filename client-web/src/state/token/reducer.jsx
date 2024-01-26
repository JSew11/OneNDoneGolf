import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  REFRESH_TOKEN,
} from 'src/utils/constants/actionTypes';

const token = sessionStorage.getItem('token');

const initialState = token ? {isLoggedIn: true, access: token} : {isLoggedIn: false, access: null}

export default function auth(state=initialState, { type, payload }) {
  switch (type) {
    case REGISTER_SUCCESS:
      return {
        isLoggedIn: true,
        access: payload.access,
      };
    case REGISTER_FAIL:
      return {
        isLoggedIn: false,
        access: null,
      };
    case LOGIN_SUCCESS:
      return {
        isLoggedIn: true,
        access: payload.access,
      };
    case LOGIN_FAIL:
      return {
        isLoggedIn: false,
        access: null,
      };
    case LOGOUT:
      return {
        isLoggedIn: false,
        access: null,
      };
    case REFRESH_TOKEN: 
      return {
        isLoggedIn: true,
        access: payload.access,
      }
    default:
      return state;
  }
}