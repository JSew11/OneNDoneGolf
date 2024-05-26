import { privateAxios } from 'src/api/axios.jsx';

import { GOLF_PICKEM_API_BASE_URL, PICK_API_BASE_URL } from 'src/assets/constants/apiUrls';

const BASE_URL = GOLF_PICKEM_API_BASE_URL + PICK_API_BASE_URL

const list = async () => {
    return await privateAxios.get(BASE_URL);
};

const create = async (seasonId, tournamentId, primarySelectionGolferId, backupSelectionGolferId) => {
    const newPickData = {
        season_id: seasonId,
        tournament_id: tournamentId,
        primary_selection_golfer_id: primarySelectionGolferId,
        backup_selection_golfer_id: backupSelectionGolferId,
    };
    return await privateAxios.post(BASE_URL, newPickData);
};

const retrieve = async (pickId) => {
    return await privateAxios.get(BASE_URL + pickId + '/');
};

const changeGolfer = async (pickId, newPrimarySelectionGolferId, newBackupSelectionGolferId) => {
    const updatedPickData = {
        primary_selection_golfer_id: newPrimarySelectionGolferId,
        backup_selection_golfer_id: newBackupSelectionGolferId,
    };
    return await privateAxios.patch(BASE_URL + pickId + '/', updatedPickData);
};

const destroy = async (pickId) => {
    return await privateAxios.delete(BASE_URL + pickId);
};

const PicksApi = {
    list,
    create,
    retrieve,
    changeGolfer,
    destroy
};

export default PicksApi;