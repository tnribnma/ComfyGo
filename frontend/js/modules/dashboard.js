document.addEventListener('DOMContentLoaded', async () => {
  if (!Storage.isAuthenticated()) {
    window.location.href = 'login.html';
    return;
  }

  setupLogout();
  loadDashboardStats();
});

function setupLogout() {
  const logoutLink = document.querySelector('.logout');
  
  if (logoutLink) {
    logoutLink.addEventListener('click', (e) => {
      e.preventDefault();
      if (confirm('Are you sure you want to log out?')) {
        Storage.clear();
        window.location.href = 'index.html';
      }
    });
  }
}

async function loadDashboardStats() {
  try {
    const stats = await apiClient.get('/admin/stats');
    
    updateStatElement('stat-bookings', stats.bookings);
    updateStatElement('stat-revenue', '$' + formatNumber(stats.revenue || 0));
    updateStatElement('stat-hotels', stats.hotels);
    updateStatElement('stat-rating', stats.rating || '4.8/5');
    
    try {
      const bookings = await apiClient.get('/bookings/?limit=3');
      loadRecentBookings(bookings.items || []);
    } catch (e) {
      console.log('Could not load bookings');
    }
    
  } catch (error) {
    console.error('Failed to load dashboard stats:', error);
    showToast('Could not load dashboard data');
  }
}

function updateStatElement(elementId, value) {
  const element = document.querySelector('[data-' + elementId.replace('stat-', '') + ']');
  if (element) {
    const strong = element.querySelector('strong');
    if (strong) {
      strong.textContent = value;
    }
  }
}

function loadRecentBookings(bookings) {
  const container = document.querySelector('.panel');
  if (!container || bookings.length === 0) return;
  
  const panels = document.querySelectorAll('.panel');
  let bookingPanel = null;
  
  panels.forEach(panel => {
    if (panel.querySelector('h2') && panel.querySelector('h2').textContent.includes('Recent')) {
      bookingPanel = panel;
    }
  });
  
  if (!bookingPanel) return;
  
  const html = bookings.map(booking => `
    <div class="booking-item">
      <span>
        <b>${booking.customer_name || 'Guest'}</b><br>
        <small class="muted">${booking.hotel_name || 'Hotel'} · ${booking.check_in_date} – ${booking.check_out_date}</small>
      </span>
      <span class="status ${booking.booking_status ? booking.booking_status.toLowerCase() : 'pending'}">
        ${booking.booking_status || 'Pending'}
      </span>
    </div>
  `).join('');
  
  const items = bookingPanel.querySelectorAll('.booking-item');
  if (items.length > 0) {
    items.forEach(item => item.remove());
  }
  
  const div = document.createElement('div');
  div.innerHTML = html;
  bookingPanel.appendChild(div);
}

function formatNumber(num) {
  return num.toLocaleString('en-US', { maximumFractionDigits: 0 });
}

function showToast(message) {
  const toast = document.querySelector('#toast');
  if (toast) {
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  }
}