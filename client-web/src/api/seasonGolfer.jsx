import { privateAxios } from 'src/api/axios';
import { 
  GOLF_PICKEM_API_BASE_URL,
  SEASON_API_BASE_URL,
  GOLFER_API_BASE_URL,
} from 'src/assets/constants/apiUrls';

const list = async (seasonId) => {
  return await privateAxios.get(
    GOLF_PICKEM_API_BASE_URL +
    SEASON_API_BASE_URL + seasonId + '/' +
    GOLFER_API_BASE_URL
  );
}

const SeasonGolfersApi = {
  list,
};

export default SeasonGolfersApi;