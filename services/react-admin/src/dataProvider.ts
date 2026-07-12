import simpleRestProvider from 'ra-data-simple-rest';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001/api';

const httpClient = (url: string, options: any = {}) => {
    const token = localStorage.getItem('access_token');
    const headers = new Headers(options.headers || {});
    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }
    return fetch(url, { ...options, headers });
};

const baseProvider = simpleRestProvider(apiUrl, httpClient);

export const dataProvider = {
    // ---- GET LIST ----
    getList: async (resource, params) => {
        if (['users', 'tariffs', 'carriers', 'orders'].includes(resource)) {
            let url = `${apiUrl}/${resource}/`;
            const queryParams: string[] = [];

            // Сортировка
            if (params.sort) {
                const { field, order } = params.sort;
                const ordering = order === 'ASC' ? field : `-${field}`;
                queryParams.push(`ordering=${ordering}`);
            }

            // Фильтры (можно добавить позже)
            // if (params.filter) { ... }

            if (queryParams.length) {
                url += '?' + queryParams.join('&');
            }

            const response = await httpClient(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const json = await response.json();

            let data = json;
            // Для users ответ обёрнут в { users: [...] }
            if (resource === 'users' && json.users) {
                data = json.users;
            }
            // Для остальных ресурсов (ModelViewSet) ответ — массив
            return {
                data: data,
                total: data.length,
            };
        }
        return baseProvider.getList(resource, params);
    },

    // ---- GET ONE ----
    getOne: async (resource, params) => {
        if (resource === 'users') {
            const url = `${apiUrl}/users/${params.id}/`;
            const response = await httpClient(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const json = await response.json();
            // Ваш UserIdView возвращает объект без обёртки или с обёрткой user
            const data = json.user || json;
            return { data };
        }
        return baseProvider.getOne(resource, params);
    },

    // ---- CREATE ----
    create: async (resource, params) => {
        // Для users используем /register/
        if (resource === 'users') {
            const url = `${apiUrl}/users/register/`;
            const response = await httpClient(url, {
                method: 'POST',
                body: JSON.stringify(params.data),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const json = await response.json();
            // Ответ от регистрации: { user: {...}, message: '...' }
            return { data: json.user };
        }
        // Для остальных ресурсов используем стандартный create
        return baseProvider.create(resource, params);
    },

    // ---- UPDATE ----
    update: async (resource, params) => {
        // Для users используем /update/<id>/
        if (resource === 'users') {
            const url = `${apiUrl}/update/${params.id}/`;
            const response = await httpClient(url, {
                method: 'PUT',
                body: JSON.stringify(params.data),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const json = await response.json();
            // Предполагаем, что ответ содержит обновлённого пользователя
            return { data: json.user || json };
        }
        return baseProvider.update(resource, params);
    },

    // ---- DELETE ----
    delete: async (resource, params) => {
        // Для users используем /delete/<id>/
        if (resource === 'users') {
            const url = `${apiUrl}/delete/${params.id}/`;
            const response = await httpClient(url, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return { data: { id: params.id } };
        }
        return baseProvider.delete(resource, params);
    },

    // ---- Остальные методы (getMany, getManyReference, updateMany, deleteMany) ----
    getMany: (resource, params) => baseProvider.getMany(resource, params),
    getManyReference: (resource, params) => baseProvider.getManyReference(resource, params),
    updateMany: (resource, params) => baseProvider.updateMany(resource, params),
    deleteMany: (resource, params) => baseProvider.deleteMany(resource, params),
};