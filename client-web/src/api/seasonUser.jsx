import { privateAxios } from 'src/api/axios.jsx';
import {
  GOLF_PICKEM_API_BASE_URL,
  SEASON_API_BASE_URL,
  USER_API_BASE_URL
} from 'src/assets/constants/apiUrls.jsx';

const list = async (seasonId) => {
  return await privateAxios.get(
    GOLF_PICKEM_API_BASE_URL +
    SEASON_API_BASE_URL + seasonId + '/' +
    USER_API_BASE_URL
  )
};

const retrieve = async (seasonId, userId) => {
  return await privateAxios.get(
    GOLF_PICKEM_API_BASE_URL + 
    SEASON_API_BASE_URL + seasonId + '/' +
    USER_API_BASE_URL + userId
  )
};

const SeasonUsersApi = {
  list,
  retrieve,
};

export default SeasonUsersApi;