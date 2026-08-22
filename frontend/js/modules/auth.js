document.addEventListener('DOMContentLoaded', () => {
    const token = Storage.getToken();
    const role = Storage.getRole();
    const navAuth = document.getElementById('nav-auth');
    const homeActions = document.getElementById('home-actions');
    const logoutBtn = document.getElementById('logout-btn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            Storage.clear();
            window.location.href = 'login.html';
        });
    }

    if (navAuth) {
        if (token) {
            navAuth.innerHTML = `
                <span class="navbar-text text-light me-3">Role: ${role}</span>
                <a href="dashboard.html" class="btn btn-outline-light btn-sm">Dashboard</a>
            `;
        } else {
            navAuth.innerHTML = `<a href="login.html" class="btn btn-outline-light btn-sm">Login</a>`;
        }
    }

    if (homeActions) {
        if (token) {
            homeActions.innerHTML = `<a href="dashboard.html" class="btn btn-primary btn-lg">Go to Dashboard</a>`;
        } else {
            homeActions.innerHTML = `<a href="login.html" class="btn btn-primary btn-lg">Login to Continue</a>`;
        }
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const role = document.getElementById('role').value;
            const alertBox = document.getElementById('alert-box');

            try {
                const res = await apiClient.post(`/auth/login/${role}`, { 
                    [`${role}_email`]: email, 
                    [`${role}_password`]: password 
                });
                
                Storage.setToken(res.access_token);
                Storage.setRole(res.role);
                
                if (role === 'admin') {
                    window.location.href = 'dashboard.html';
                } else {
                    window.location.href = 'index.html';
                }
            } catch (error) {
                alertBox.classList.remove('d-none');
                alertBox.innerText = error.message;
            }
        });
    }

    const protectedPages = ['dashboard.html', 'hotels.html', 'bookings.html'];
    if (protectedPages.some(p => window.location.pathname.includes(p))) {
        if (!token) {
            window.location.href = 'login.html';
        }
    }
});