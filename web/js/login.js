// Login page functionality

const loginForm = document.getElementById('loginForm');
const errorMessage = document.getElementById('errorMessage');
const loginBtnText = document.getElementById('loginBtnText');
const loginBtnSpinner = document.getElementById('loginBtnSpinner');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Reset error message
    errorMessage.classList.remove('show');
    errorMessage.textContent = '';
    
    // Get form data
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Show loading state
    loginBtnText.style.display = 'none';
    loginBtnSpinner.style.display = 'inline-block';
    loginForm.querySelector('button[type="submit"]').disabled = true;
    
    try {
        // Call login API
        const response = await apiService.login(email, password);
        
        // Store token
        apiService.setToken(response.access_token);
        
        // Redirect to dashboard
        window.location.href = '/dashboard.html';
    } catch (error) {
        // Show error message
        errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
        errorMessage.classList.add('show');
        
        // Reset button state
        loginBtnText.style.display = 'inline';
        loginBtnSpinner.style.display = 'none';
        loginForm.querySelector('button[type="submit"]').disabled = false;
    }
});

// Redirect to dashboard if already logged in
if (isAuthenticated()) {
    window.location.href = '/dashboard.html';
}

