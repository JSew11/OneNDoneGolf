import { privateAxios } from 'src/api/axios.jsx';

import { GOLF_PICKEM_API_BASE_URL, SEASON_API_BASE_URL } from 'src/assets/constants/apiUrls';

const BASE_URL = GOLF_PICKEM_API_BASE_URL + SEASON_API_BASE_URL

const list = async () => {
    return await privateAxios.get(BASE_URL);
};

const create = async (newSeasonData) => {
    return await privateAxios.post(BASE_URL, newSeasonData);
};

const retrieve = async (seasonId) => {
    return await privateAxios.get(BASE_URL + seasonId + '/');
};

const partialUpdate = async (seasonId, updatedSeasonData) => {
    return await privateAxios.patch(BASE_URL + seasonId + '/', updatedSeasonData);
};

const destroy = async (seasonId) => {
    return await privateAxios.delete(BASE_URL + seasonId);
};

const active = async () => {
    return await privateAxios.get(BASE_URL + 'active/');
};

const nextTournament = async (seasonId) => {
    return await privateAxios.get(BASE_URL + seasonId + '/next-tournament/');
};

const standings = async (seasonId) => {
    return await privateAxios.get(BASE_URL + seasonId + '/users/');
};

const SeasonsApi = {
    list,
    create,
    retrieve,
    partialUpdate,
    destroy,
    active,
    nextTournament,
    standings,
};

export default SeasonsApi;