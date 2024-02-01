import { publicAxios } from 'src/api/axios.jsx';

import {
  REGISTER_API_URL,
  LOGIN_API_URL,
  LOGOUT_API_URL,
  REFRESH_TOKEN_API_URL
} from 'src/assets/constants/apiUrls';

const register = async (userRegistrationData) => {
  return await publicAxios.post(REGISTER_API_URL, userRegistrationData)
  .then(
    (response) => {
      if (response.data.access) {
        sessionStorage.setItem('token', response.data.access);
      }

      return response;
    },
    (error) => error
  );
};

const login = async (email, password) => {
  return await publicAxios.post(LOGIN_API_URL, {
    email: email,
    password: password,
  })
  .then(
    (response) => {
      if (response.data.access) {
        sessionStorage.setItem('token', response.data.access);
      }

      return response;
    }
  );
};

const logout = async () => {
  return await publicAxios.post(LOGOUT_API_URL)
  .then(
    (response) => {
      sessionStorage.removeItem('token');
      return response;
    }
  );
};

const refreshToken = async () => {
  return await publicAxios.post(REFRESH_TOKEN_API_URL)
  .then(
    (response) => {
      if (response.data.access) {
        sessionStorage.setItem('token', response.data.access);
      }

      return response;
    },
    (error) => error
  );
}

const AuthApi = {
  register,
  login,
  logout,
  refreshToken,
};

export default AuthApi;