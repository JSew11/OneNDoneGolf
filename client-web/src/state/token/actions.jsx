import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  REFRESH_TOKEN,
} from 'src/utils/constants/actionTypes';
import AuthApi from 'src/api/auth';

export const register = (userRegistrationData) => (dispatch) => {
  return AuthApi.register(userRegistrationData).then(
    (response) => {
      dispatch({
        type: REGISTER_SUCCESS,
        payload: {
          access: response.data.access
        },
      });

      return response;
    },
    (error) => {
      dispatch({
        type: REGISTER_FAIL,
      });

      return error;
    }
  );
};

export const login = (email, password) => (dispatch) => {
  return AuthApi.login(email, password).then(
    (response) => {
      if (response.data?.access) {
        dispatch({
          type: LOGIN_SUCCESS,
          payload: {
            access: response.data.access
          },
        });
      }

      return response;
    },
    (error) => {
      dispatch({
        type: LOGIN_FAIL,
      });

      return error;
    }
  );
}

export const logout = () => (dispatch) => {
  AuthApi.logout().then(
    (response) => {  
      dispatch({
        type: LOGOUT,
      });

      return response;
    },
    (error) => error
  );
};

export const refreshToken = (access) => (dispatch) => {
  dispatch({
    type: REFRESH_TOKEN,
    payload: {
      access: access,
    },
  });
}