import { privateAxios } from 'src/api/axios.jsx';

import { SEASON_API_BASE_URL } from 'src/assets/constants/apiUrls';

const list = async () => {
    return await privateAxios.get(SEASON_API_BASE_URL);
};

const create = async (newSeasonData) => {
    return await privateAxios.post(SEASON_API_BASE_URL, newSeasonData);
};

const retrieve = async (seasonId) => {
    return await privateAxios.get(SEASON_API_BASE_URL + seasonId + '/');
};

const partialUpdate = async (seasonId, updatedSeasonData) => {
    return await privateAxios.patch(SEASON_API_BASE_URL + seasonId + '/', updatedSeasonData);
};

const destroy = async (seasonId) => {
    return await privateAxios.delete(SEASON_API_BASE_URL + seasonId);
}

const active = async () => {
    return await privateAxios.get(SEASON_API_BASE_URL + 'active/');
}

const nextTournament = async (seasonId) => {
    return await privateAxios.get(SEASON_API_BASE_URL + seasonId + '/next-tournament/');
}

const SeasonsApi = {
    list,
    create,
    retrieve,
    partialUpdate,
    destroy,
    active,
    nextTournament,
};

export default SeasonsApi;