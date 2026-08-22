const Storage = {
    setToken: (token) => localStorage.setItem('comfygo_token', token),
    getToken: () => localStorage.getItem('comfygo_token'),
    setRole: (role) => localStorage.setItem('comfygo_role', role),
    getRole: () => localStorage.getItem('comfygo_role'),
    clear: () => {
        localStorage.removeItem('comfygo_token');
        localStorage.removeItem('comfygo_role');
    }
};