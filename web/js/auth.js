// Authentication utility functions

// Check if user is authenticated
function isAuthenticated() {
    return apiService.getToken() !== null;
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        // Redirect to root (which serves index.html from backend)
        window.location.href = '/';
        return false;
    }
    return true;
}

// Logout function
function logout() {
    apiService.setToken(null);
    // Redirect to root (which serves index.html from backend)
    window.location.href = '/';
}

// Initialize auth check on protected pages
function initAuth() {
    // Check if we're on a protected page
    const protectedPages = ['dashboard.html', 'meal-plans.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    if (protectedPages.includes(currentPage)) {
        if (!requireAuth()) {
            return;
        }
    }
    
    // Setup logout button if it exists
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAuth);
} else {
    initAuth();
}

