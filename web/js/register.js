// Register page functionality

const registerForm = document.getElementById('registerForm');
const errorMessage = document.getElementById('errorMessage');
const registerBtnText = document.getElementById('registerBtnText');
const registerBtnSpinner = document.getElementById('registerBtnSpinner');

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Reset error message
    errorMessage.classList.remove('show');
    errorMessage.textContent = '';
    
    // Get form data
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        height: parseFloat(document.getElementById('height').value),
        weight: parseFloat(document.getElementById('weight').value),
        activity_level: document.getElementById('activityLevel').value,
        health_goal: document.getElementById('healthGoal').value,
    };
    
    // Show loading state
    registerBtnText.style.display = 'none';
    registerBtnSpinner.style.display = 'inline-block';
    registerForm.querySelector('button[type="submit"]').disabled = true;
    
    try {
        // Call register API
        const response = await apiService.register(formData);
        
        // Store token
        apiService.setToken(response.access_token);
        
        // Redirect to dashboard
        window.location.href = '/dashboard.html';
}
    } catch (error) {
        // Show error message
        errorMessage.textContent = error.message || 'Registration failed. Please try again.';
        errorMessage.classList.add('show');
        
        // Reset button state
        registerBtnText.style.display = 'inline';
        registerBtnSpinner.style.display = 'none';
        registerForm.querySelector('button[type="submit"]').disabled = false;
    }
});

// Redirect to dashboard if already logged in
if (isAuthenticated()) {
    window.location.href = '/dashboard.html';
}

