let hotelModal;

document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.getElementById('hotels-table-body');
    if (!tableBody) return; 

    hotelModal = new bootstrap.Modal(document.getElementById('hotelModal'));
    
    await loadHotels();
});

async function loadHotels() {
    try {
        const hotels = await apiClient.get('/hotels/');
        const tableBody = document.getElementById('hotels-table-body');
        
        if (hotels.items.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No hotels found.</td></tr>';
            return;
        }

        tableBody.innerHTML = hotels.items.map(h => `
            <tr>
                <td>${h.hotel_id}</td>
                <td>${h.hotel_name}</td>
                <td>${h.hotel_city}</td>
                <td>${h.hotel_country}</td>
                <td>${h.hotel_rating || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="editHotel(${h.hotel_id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteHotel(${h.hotel_id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        alert('Error loading hotels: ' + error.message);
    }
}

function resetForm() {
    document.getElementById('hotel-form').reset();
    document.getElementById('hotel_id').value = '';
    document.getElementById('modalTitle').innerText = 'Add Hotel';
}

async function editHotel(id) {
    try {
        const hotels = await apiClient.get('/hotels/');
        const hotel = hotels.items.find(h => h.hotel_id === id);
        
        if (!hotel) return;

        document.getElementById('hotel_id').value = hotel.hotel_id;
        document.getElementById('hotel_name').value = hotel.hotel_name;
        document.getElementById('hotel_address').value = hotel.hotel_address;
        document.getElementById('hotel_city').value = hotel.hotel_city;
        document.getElementById('hotel_country').value = hotel.hotel_country;
        document.getElementById('hotel_rating').value = hotel.hotel_rating || '';
        
        document.getElementById('modalTitle').innerText = 'Edit Hotel';
        hotelModal.show();
    } catch (error) {
        alert('Error fetching hotel: ' + error.message);
    }
}

async function saveHotel() {
    const id = document.getElementById('hotel_id').value;
    const data = {
        hotel_name: document.getElementById('hotel_name').value,
        hotel_address: document.getElementById('hotel_address').value,
        hotel_city: document.getElementById('hotel_city').value,
        hotel_country: document.getElementById('hotel_country').value,
        hotel_rating: document.getElementById('hotel_rating').value || null,
    };

    try {
        if (id) {
            await apiClient.put(`/hotels/${id}`, data);
        } else {
            await apiClient.post('/hotels/', data);
        }
        hotelModal.hide();
        await loadHotels();
    } catch (error) {
        alert('Error saving hotel: ' + error.message);
    }
}

async function deleteHotel(id) {
    if (!confirm('Are you sure you want to delete this hotel?')) return;
    try {
        await apiClient.delete(`/hotels/${id}`);
        await loadHotels();
    } catch (error) {
        alert('Error deleting hotel: ' + error.message);
    }
}