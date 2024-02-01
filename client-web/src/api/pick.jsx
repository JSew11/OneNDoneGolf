import { privateAxios } from 'src/api/axios.jsx';

import { PICK_API_BASE_URL } from 'src/assets/constants/apiUrls';

const list = async () => {
    return await privateAxios.get(PICK_API_BASE_URL);
};

const create = async (seasonId, tournamentId, golferId) => {
    const newPickData = {
        season_id: seasonId,
        tournament_id: tournamentId,
        golfer_id: golferId,
    };
    return await privateAxios.post(PICK_API_BASE_URL, newPickData);
};

const retrieve = async (pickId) => {
    return await privateAxios.get(PICK_API_BASE_URL + pickId + '/');
};

const changeGolfer = async (pickId, newGolferId) => {
    const updatedPickData = {
        golfer_id: newGolferId
    };
    return await privateAxios.patch(PICK_API_BASE_URL + pickId + '/', updatedPickData);
};

const destroy = async (pickId) => {
    return await privateAxios.delete(PICK_API_BASE_URL + pickId);
}

const SeasonsApi = {
    list,
    create,
    retrieve,
    changeGolfer,
    destroy
};

export default SeasonsApi;