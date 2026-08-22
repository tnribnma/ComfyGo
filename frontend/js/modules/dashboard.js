document.addEventListener('DOMContentLoaded', async () => {
    const statCustomers = document.getElementById('stat-customers');
    const statHotels = document.getElementById('stat-hotels');
    const statBookings = document.getElementById('stat-bookings');
    const statPayments = document.getElementById('stat-payments');
    const activityFeed = document.getElementById('activity-feed');

    if (!statCustomers) return; 

    try {
        const stats = await apiClient.get('/admin/stats');
        statCustomers.innerText = stats.customers;
        statHotels.innerText = stats.hotels;
        statBookings.innerText = stats.bookings;
        statPayments.innerText = stats.payments;

        const logs = await apiClient.get('/admin/recent-activity?limit=5');
        
        if (logs.length === 0) {
            activityFeed.innerHTML = '<p class="text-muted">No recent activity.</p>';
            return;
        }

        activityFeed.innerHTML = logs.map(log => `
            <div class="activity-item">
                <div class="d-flex justify-content-between">
                    <strong>${log.action} ${log.entity_type || ''}</strong>
                    <small class="text-muted">${new Date(log.timestamp).toLocaleString()}</small>
                </div>
                <div class="mt-1">
                    <span class="badge bg-${log.user_role === 'admin' ? 'dark' : 'primary'}">${log.user_role || 'Unknown'}</span>
                    <span class="text-muted">User ID: ${log.user_id || 'N/A'}</span> 
                    <span class="text-muted">| ${log.request_method} ${log.request_path}</span>
                    <span class="badge bg-${log.status_code < 400 ? 'success' : 'danger'} ms-2">${log.status_code}</span>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
});