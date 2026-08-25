let hotelModal;

document.addEventListener('DOMContentLoaded', async () => {
  if (!Storage.isAuthenticated()) {
    window.location.href = 'login.html';
    return;
  }

  setupModalIfNeeded();
  setupFormHandlers();
  loadHotels();
});

function setupModalIfNeeded() {
  const modalEl = document.getElementById('hotelModal');
  if (modalEl && typeof bootstrap !== 'undefined') {
    hotelModal = new bootstrap.Modal(modalEl);
  }
}

function setupFormHandlers() {
  const saveBtn = document.querySelector('[data-save-hotel]');
  const resetBtn = document.querySelector('[data-reset-hotel]');
  
  if (saveBtn) {
    saveBtn.addEventListener('click', saveHotel);
  }
  
  if (resetBtn) {
    resetBtn.addEventListener('click', resetForm);
  }
}

function resetForm() {
  const form = document.getElementById('hotel-form');
  if (form) {
    form.reset();
    document.getElementById('hotel_id').value = '';
    const title = document.getElementById('modalTitle');
    if (title) title.textContent = 'Add Hotel';
  }
}

async function loadHotels() {
  try {
    const data = await apiClient.get('/hotels/?limit=100');
    const hotels = data.items || [];
    const tableBody = document.getElementById('hotels-table-body');
    
    if (!tableBody) return;
    
    if (hotels.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No hotels found.</td></tr>';
      return;
    }

    tableBody.innerHTML = hotels.map(hotel => `
      <tr>
        <td>${hotel.hotel_id}</td>
        <td>${hotel.hotel_name}</td>
        <td>${hotel.hotel_city}</td>
        <td>${hotel.hotel_country}</td>
        <td>${hotel.hotel_rating || 'N/A'}</td>
        <td>
          <button class="btn btn-sm btn-warning" onclick="editHotel(${hotel.hotel_id})">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="deleteHotel(${hotel.hotel_id})">Delete</button>
        </td>
      </tr>
    `).join('');
  } catch (error) {
    console.error('Error loading hotels:', error);
    const tableBody = document.getElementById('hotels-table-body');
    if (tableBody) {
      tableBody.innerHTML = '<tr><td colspan="6" class="text-danger">Failed to load hotels.</td></tr>';
    }
  }
}

async function editHotel(id) {
  try {
    const hotel = await apiClient.get('/hotels/' + id);
    
    document.getElementById('hotel_id').value = hotel.hotel_id;
    document.getElementById('hotel_name').value = hotel.hotel_name;
    document.getElementById('hotel_address').value = hotel.hotel_address;
    document.getElementById('hotel_city').value = hotel.hotel_city;
    document.getElementById('hotel_country').value = hotel.hotel_country;
    document.getElementById('hotel_rating').value = hotel.hotel_rating || '';
    document.getElementById('hotel_phone').value = hotel.hotel_phone || '';
    document.getElementById('hotel_email').value = hotel.hotel_email || '';
    document.getElementById('hotel_description').value = hotel.hotel_description || '';
    
    document.getElementById('modalTitle').textContent = 'Edit Hotel';
    
    if (hotelModal) {
      hotelModal.show();
    }
  } catch (error) {
    alert('Error loading hotel: ' + error.message);
  }
}

async function saveHotel() {
  const id = document.getElementById('hotel_id').value;
  
  const data = {
    hotel_name: document.getElementById('hotel_name').value,
    hotel_address: document.getElementById('hotel_address').value,
    hotel_city: document.getElementById('hotel_city').value,
    hotel_country: document.getElementById('hotel_country').value,
    hotel_rating: parseFloat(document.getElementById('hotel_rating').value) || null,
    hotel_phone: document.getElementById('hotel_phone').value || null,
    hotel_email: document.getElementById('hotel_email').value || null,
    hotel_description: document.getElementById('hotel_description').value || null,
  };

  try {
    if (id) {
      await apiClient.put('/hotels/' + id, data);
      alert('Hotel updated successfully!');
    } else {
      await apiClient.post('/hotels/', data);
      alert('Hotel created successfully!');
    }
    
    if (hotelModal) {
      hotelModal.hide();
    }
    
    resetForm();
    await loadHotels();
  } catch (error) {
    alert('Error saving hotel: ' + error.message);
  }
}

async function deleteHotel(id) {
  if (!confirm('Are you sure you want to delete this hotel?')) return;
  
  try {
    await apiClient.delete('/hotels/' + id);
    alert('Hotel deleted successfully!');
    await loadHotels();
  } catch (error) {
    alert('Error deleting hotel: ' + error.message);
  }
}