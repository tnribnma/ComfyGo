const API_BASE_URL = 'http://localhost:8000/api/v1';

const apiClient = {
    request: async (endpoint, method = 'GET', body = null) => {
        const token = Storage.getToken();
        const headers = {
            'Content-Type': 'application/json',
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = { method, headers };
        if (body) {
            config.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        if (response.status === 401) {
            Storage.clear();
            window.location.href = 'login.html';
            throw new Error('Unauthorized');
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || errorData.message || 'API Error');
        }

        if (response.status === 204) return null; 
        return response.json();
    },

    get: (endpoint) => apiClient.request(endpoint, 'GET'),
    post: (endpoint, body) => apiClient.request(endpoint, 'POST', body),
    put: (endpoint, body) => apiClient.request(endpoint, 'PUT', body),
    delete: (endpoint) => apiClient.request(endpoint, 'DELETE'),
};