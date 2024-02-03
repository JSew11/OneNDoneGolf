import { privateAxios } from 'src/api/axios';

import { 
    GOLF_PICKEM_API_BASE_URL,
    SEASON_API_BASE_URL,
    TOURNAMENT_API_BASE_URL
} from 'src/assets/constants/apiUrls';

const availableGolfers = async (seasonId, tournamentId ) => {
    return await privateAxios.get(
        GOLF_PICKEM_API_BASE_URL +
        SEASON_API_BASE_URL + seasonId + '/' +
        TOURNAMENT_API_BASE_URL + tournamentId + '/available-golfers'
    );
};

const TournamentSeasonsApi = {
    availableGolfers,
};

export default TournamentSeasonsApi;