import { privateAxios } from 'src/api/axios.jsx';
import { GOLF_PICKEM_API_BASE_URL, SEASON_API_BASE_URL } from 'src/assets/constants/apiUrls';

const BASE_URL = GOLF_PICKEM_API_BASE_URL + SEASON_API_BASE_URL

const list = async () => {
    return await privateAxios.get(BASE_URL);
};

const create = async (name, alias, year, registrationCutoff) => {
    const newSeasonData = {
        name: name,
        alias: alias,
        year: year,
        registration_cutoff: registrationCutoff
    };
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

const activeTournament = async (seasonId) => {
    return await privateAxios.get(BASE_URL + seasonId + '/active-tournament/')
}

const setActiveSeason = async (seasonId) => {
    return await privateAxios.post(BASE_URL + 'active/' + seasonId + '/');
}

const updateOWGR = async (seasonId) => {
    return await privateAxios.post(BASE_URL + seasonId + '/owgr/')
}

const SeasonsApi = {
    list,
    create,
    retrieve,
    partialUpdate,
    destroy,
    active,
    nextTournament,
    activeTournament,
    setActiveSeason,
    updateOWGR,
};

export default SeasonsApi;