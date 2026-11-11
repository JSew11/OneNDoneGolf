import { privateAxios } from 'src/api/axios.jsx';
import { CORE_API_BASE_URL } from 'src/assets/constants/apiUrls.jsx';

const list = async () => {
    return await privateAxios.get(CORE_API_BASE_URL);
}

const me = async () => {
    return await privateAxios.get(CORE_API_BASE_URL + 'me/');
}

const retrieve = async (userId) => {
    return await privateAxios.get(CORE_API_BASE_URL + userId + '/');
}

const partialUpdate = async (userId, updatedUserData) => {
    return await privateAxios.patch(CORE_API_BASE_URL + userId + '/', updatedUserData);
}

const destroy = async (userId) => {
    return await privateAxios.delete(CORE_API_BASE_URL + userId + '/');
}

const UsersApi = {
    list,
    me,
    retrieve,
    partialUpdate,
    destroy,
};

export default UsersApi;