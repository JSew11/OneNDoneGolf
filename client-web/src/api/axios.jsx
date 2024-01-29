import axios from 'axios';

import store from 'src/state/store.jsx';
import AuthApi from 'src/api/auth.jsx';
import { refreshToken } from 'src/state/token/actions.jsx';

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;

const publicAxios = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

const privateAxios = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

privateAxios.interceptors.request.use(
  async (config) => {
    const state = store.getState();
    const accessToken = state.auth.access;

    if (accessToken && accessToken !== '') {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${accessToken}`,
      };
    }

    return config;
  },
  (error) => Promise.reject(error)
);

const { dispatch } = store;
privateAxios.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const config = error?.config;

    if (error?.response.status === 401 && !config?._retry) {
      config._retry = true;

      try {
        const response = await AuthApi.refreshToken();
        dispatch(refreshToken(response.data.access));
        config.headers = {
          ...config.headers,
          Authorization: `Bearer ${response.data.access}`,
        };
        return privateAxios(config);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export { publicAxios, privateAxios };