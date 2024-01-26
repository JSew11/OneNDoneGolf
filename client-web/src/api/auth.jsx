import { publicAxios } from 'src/api/axios.jsx';

const REGISTER_URL = 'register/';
const LOGIN_URL = 'login/';
const LOGOUT_URL = 'logout/';
const REFRESH_TOKEN_URL = 'login/refresh/';

const register = async (userRegistrationData) => {
  return await publicAxios.post(REGISTER_URL, userRegistrationData)
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

const login = async (username, password) => {
  return await publicAxios.post(LOGIN_URL, {
    username: username,
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
  return await publicAxios.post(LOGOUT_URL)
  .then(
    (response) => {
      sessionStorage.removeItem('token');
      return response;
    }
  );
};

const refreshToken = async () => {
  return await publicAxios.post(REFRESH_TOKEN_URL)
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