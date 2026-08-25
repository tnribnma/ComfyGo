document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.querySelector('[data-login]');
  const registerForm = document.querySelector('[data-register]');

  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }

  if (registerForm) {
    registerForm.addEventListener('submit', handleRegister);
  }
});

async function handleLogin(event) {
  event.preventDefault();
  
  const form = event.currentTarget;
  const email = form.querySelector('[name="email"]').value.trim();
  const password = form.querySelector('[name="password"]').value;
  const role = form.querySelector('[name="role"]').value;
  const button = form.querySelector('button[type="submit"]');
  
  const originalText = button.innerHTML;
  button.disabled = true;
  button.innerHTML = 'Signing in…';
  
  clearMessage();

  try {
    const endpoint = '/auth/login/' + role;
    const payload = {};
    payload[role + '_email'] = email;
    payload[role + '_password'] = password;
    
    const result = await apiClient.post(endpoint, payload);

    if (result.access_token) {
      Storage.setToken(result.access_token);
      Storage.setRole(result.role || role);
      if (result.refresh_token) {
        localStorage.setItem('comfygo_refresh_token', result.refresh_token);
      }
      sessionStorage.removeItem('_comfygo_redirecting');
      sessionStorage.removeItem('_comfygo_redirect_ts');
      
      showMessage('Login successful! Redirecting…', false);
      setTimeout(() => {
        window.location.href = role === 'customer' ? 'index.html' : 'dashboard.html';
      }, 800);
    }
  } catch (error) {
    showMessage(error.message || 'Login failed. Please check your credentials.', true);
    button.disabled = false;
    button.innerHTML = originalText;
  }
}

async function handleRegister(event) {
  event.preventDefault();
  
  const form = event.currentTarget;
  const password = form.querySelector('[name="password"]').value;
  const confirmPassword = form.querySelector('[name="confirmPassword"]').value;
  const button = form.querySelector('button[type="submit"]');
  
  clearMessage();

  if (password !== confirmPassword) {
    showMessage('Passwords do not match.', true);
    return;
  }

  if (password.length < 8) {
    showMessage('Password must be at least 8 characters.', true);
    return;
  }

  const originalText = button.innerHTML;
  button.disabled = true;
  button.innerHTML = 'Creating account…';

  try {
    const result = await apiClient.post('/auth/register/customer', {
      customer_name: form.querySelector('[name="name"]').value.trim(),
      customer_email: form.querySelector('[name="email"]').value.trim(),
      customer_phone: form.querySelector('[name="phone"]').value.trim() || null,
      customer_address: form.querySelector('[name="address"]').value.trim() || null,
      customer_password: password,
    });

    if (result.access_token) {
      Storage.setToken(result.access_token);
      Storage.setRole(result.role || 'customer');
      if (result.refresh_token) {
        localStorage.setItem('comfygo_refresh_token', result.refresh_token);
      }
      sessionStorage.removeItem('_comfygo_redirecting');
      sessionStorage.removeItem('_comfygo_redirect_ts');
      
      showMessage('Account created! Taking you to ComfyGo…', false);
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1000);
    }
  } catch (error) {
    showMessage(error.message || 'Registration failed. Please try again.', true);
    button.disabled = false;
    button.innerHTML = originalText;
  }
}

function showMessage(message, isError) {
  const box = document.querySelector('#auth-message');
  if (!box) return;
  
  box.textContent = message;
  box.className = 'form-message ' + (isError ? 'error' : 'success');
  box.style.display = 'block';
}

function clearMessage() {
  const box = document.querySelector('#auth-message');
  if (box) {
    box.textContent = '';
    box.className = 'form-message';
    box.style.display = 'none';
  }
}