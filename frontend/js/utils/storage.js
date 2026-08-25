const Storage = {
  setToken: (token) => {
    localStorage.setItem('comfygo_token', token);
  },
  
  getToken: () => {
    return localStorage.getItem('comfygo_token');
  },
  
  setRole: (role) => {
    localStorage.setItem('comfygo_role', role);
  },
  
  getRole: () => {
    return localStorage.getItem('comfygo_role') || 'customer';
  },
  
  clear: () => {
    localStorage.removeItem('comfygo_token');
    localStorage.removeItem('comfygo_role');
    localStorage.removeItem('comfygo_refresh_token');
  },
  
  isAuthenticated: () => {
    return !!localStorage.getItem('comfygo_token');
  }
};