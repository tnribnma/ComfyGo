const API_ROOT = 'http://localhost:8000/api/v1';

const REDIRECT_KEY = '_comfygo_redirecting';
const REDIRECT_TS_KEY = '_comfygo_redirect_ts';

function isRedirecting() {
  const val = sessionStorage.getItem(REDIRECT_KEY);
  const ts = sessionStorage.getItem(REDIRECT_TS_KEY);
  if (!val || !ts) return false;
  if (Date.now() - Number(ts) > 5000) {
    sessionStorage.removeItem(REDIRECT_KEY);
    sessionStorage.removeItem(REDIRECT_TS_KEY);
    return false;
  }
  return true;
}

function setRedirecting() {
  sessionStorage.setItem(REDIRECT_KEY, '1');
  sessionStorage.setItem(REDIRECT_TS_KEY, String(Date.now()));
}

const apiClient = {
  request: async (endpoint, method = 'GET', body = null) => {
    const headers = {
      'Content-Type': 'application/json',
    };

    const token = Storage.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      method,
      headers,
    };

    if (body) {
      config.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(API_ROOT + endpoint, config);

      if (response.status === 401) {
        const isAuthEndpoint = endpoint.includes('/auth/login') || endpoint.includes('/auth/register');
        if (!isAuthEndpoint) {
          if (!isRedirecting()) {
            setRedirecting();
            Storage.clear();
            window.location.href = 'login.html';
          }
          throw new Error('Session expired. Please log in again.');
        }
      }

      if (response.status === 204) {
        return null;
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.message || `Error: ${response.status}`);
      }

      return data;
    } catch (error) {
      if (error.message !== 'Session expired. Please log in again.') {
        console.error('API Error:', error);
      }
      throw error;
    }
  },

  get: (endpoint) => apiClient.request(endpoint, 'GET'),
  post: (endpoint, body) => apiClient.request(endpoint, 'POST', body),
  put: (endpoint, body) => apiClient.request(endpoint, 'PUT', body),
  delete: (endpoint) => apiClient.request(endpoint, 'DELETE'),
};
