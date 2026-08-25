document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  setupMenuToggle();
});

function setupNavigation() {
  const actions = document.querySelector('.nav-actions');
  if (!actions) return;
  const token = Storage.getToken();
  if (token && actions.querySelector('a[href="login.html"]')) {
    const role = Storage.getRole();
    if (role === 'admin' || role === 'employee') {
      actions.innerHTML =
        '<a href="dashboard.html">Dashboard</a>' +
        '<button class="btn btn-ghost" id="logout-btn">Log out</button>';
    } else {
      actions.innerHTML =
        '<a href="my-account.html" style="font-weight:700;color:var(--forest)"><i class="bi bi-person-circle"></i> My Account</a>' +
        '<button class="btn btn-ghost" id="logout-btn">Log out</button>';
    }
    var btn = document.getElementById('logout-btn');
    if (btn) btn.addEventListener('click', function () {
      if (confirm('Log out?')) { Storage.clear(); window.location.href = 'index.html'; }
    });
  }
}

function setupMenuToggle() {
  var toggle = document.querySelector('[data-menu]');
  var navLinks = document.querySelector('#navLinks');
  if (toggle && navLinks) {
    toggle.addEventListener('click', function () { navLinks.classList.toggle('open'); });
  }
}

function showToast(message) {
  var toast = document.querySelector('#toast');
  if (!toast) return;
  toast.textContent = message || 'Done!';
  toast.classList.add('show');
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 3000);
}

function escapeHtml(text) {
  var d = document.createElement('div');
  d.textContent = text || '';
  return d.innerHTML;
}
