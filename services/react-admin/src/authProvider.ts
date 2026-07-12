import { AuthProvider } from 'react-admin';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001/api';

export const authProvider: AuthProvider = {
    login: async ({ username, password }) => {
        const response = await fetch(`${apiUrl}/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (response.status < 200 || response.status >= 300) {
            throw new Error('Invalid credentials');
        }
        const { access, refresh } = await response.json();
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        return Promise.resolve();
    },
    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return Promise.resolve();
    },
    checkAuth: () =>
        localStorage.getItem('access_token') ? Promise.resolve() : Promise.reject(),
    checkError: (error) => {
        const status = error.status;
        if (status === 401 || status === 403) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            return Promise.reject();
        }
        return Promise.resolve();
    },
    getPermissions: () => Promise.resolve(),
};
