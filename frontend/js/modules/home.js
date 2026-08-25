document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  setupSearchForm();
  loadFeaturedHotels();
  setupHeartButtons();
});

function setupNavigation() {
  const actions = document.querySelector('.nav-actions');
  if (!actions) return;

  const token = Storage.getToken();
  
  if (token) {
    actions.innerHTML = `
      <a href="dashboard.html">Dashboard</a>
      <button class="btn btn-ghost" id="logout-btn">Log out</button>
    `;
    
    document.getElementById('logout-btn').addEventListener('click', () => {
      if (confirm('Log out?')) {
        Storage.clear();
        window.location.href = 'index.html';
      }
    });
  } else {
    actions.innerHTML = `
      <a href="login.html">Log in</a>
      <a class="btn btn-primary" href="register.html">Sign up</a>
    `;
  }
}

function setupSearchForm() {
  const form = document.querySelector('[data-search]');
  
  if (form) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const input = form.querySelector('input');
      const destination = input.value.trim();
      
      if (destination) {
        window.location.href = 'hotels.html?city=' + encodeURIComponent(destination);
      } else {
        showToast('Please enter a destination.');
      }
    });
  }
}

function setupHeartButtons() {
  const hearts = document.querySelectorAll('[data-heart]');
  
  hearts.forEach((button) => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleFavorite(button);
    });
  });
}

function toggleFavorite(button) {
  const icon = button.querySelector('i');
  const isFilled = icon.classList.contains('bi-heart-fill');
  
  if (isFilled) {
    icon.classList.remove('bi-heart-fill');
    icon.classList.add('bi-heart');
    icon.style.color = '';
    showToast('Removed from saved stays.');
  } else {
    icon.classList.add('bi-heart-fill');
    icon.classList.remove('bi-heart');
    icon.style.color = '#e8783c';
    showToast('Added to your saved stays.');
  }
}

async function loadFeaturedHotels() {
  try {
    const data = await apiClient.get('/hotels/?limit=6');
    const hotels = data.items || [];
    
    console.log('Loaded ' + hotels.length + ' hotels');
  } catch (error) {
    console.error('Could not load hotels:', error);
  }
}

function showToast(message = 'Done!') {
  const toast = document.querySelector('#toast');
  if (!toast) return;
  
  toast.textContent = message;
  toast.classList.add('show');
  
  clearTimeout(window.toastTimeout);
  window.toastTimeout = setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}