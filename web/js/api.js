// API Configuration
// Use relative path when served from backend, or absolute URL for standalone
const API_CONFIG = {
    baseUrl: window.location.origin + '/api/v1',
    // Falls back to localhost if needed (for development)
    // baseUrl: 'http://localhost:8000/api/v1',
};

// API Service Class
class ApiService {
    constructor() {
        this.baseUrl = API_CONFIG.baseUrl;
    }

    // Get authentication token from localStorage
    getToken() {
        return localStorage.getItem('auth_token');
    }

    // Set authentication token in localStorage
    setToken(token) {
        if (token) {
            localStorage.setItem('auth_token', token);
        } else {
            localStorage.removeItem('auth_token');
        }
    }

    // Get headers with authentication
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        };

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return headers;
    }

    // Generic request method
    async request(method, endpoint, body = null) {
        const url = `${this.baseUrl}${endpoint}`;
        const options = {
            method: method,
            headers: this.getHeaders(),
        };

        if (body && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(url, options);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || data.message || `Request failed with status ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // Auth endpoints
    async login(email, password) {
        return this.request('POST', '/auth/login', { email, password });
    }

    async register(userData) {
        return this.request('POST', '/auth/register', userData);
    }

    // User endpoints
    async getProfile() {
        return this.request('GET', '/users/profile');
    }

    async updateProfile(userData) {
        return this.request('PUT', '/users/profile', userData);
    }

    // Meal Plan endpoints
    async getMealPlans(startDate = null, endDate = null) {
        let endpoint = '/meal-plans';
        const params = [];
        
        if (startDate) {
            params.push(`start_date=${encodeURIComponent(startDate.toISOString())}`);
        }
        if (endDate) {
            params.push(`end_date=${encodeURIComponent(endDate.toISOString())}`);
        }
        
        if (params.length > 0) {
            endpoint += '?' + params.join('&');
        }
        
        return this.request('GET', endpoint);
    }

    async generateMealPlan(startDate, endDate, goal = null) {
        let endpoint = `/meal-plans/generate?start_date=${encodeURIComponent(startDate.toISOString())}&end_date=${encodeURIComponent(endDate.toISOString())}`;
        
        if (goal) {
            endpoint += `&goal=${encodeURIComponent(goal)}`;
        }
        
        return this.request('POST', endpoint);
    }

    // Nutrition endpoints
    async analyzeNutrition(foods) {
        return this.request('POST', '/nutrition/analyze', { foods });
    }

    // Recommendations endpoints
    async getRecommendations(mealType, date = null) {
        let endpoint = `/recommendations?meal_type=${encodeURIComponent(mealType)}`;
        
        if (date) {
            endpoint += `&date=${encodeURIComponent(date.toISOString())}`;
        }
        
        return this.request('GET', endpoint);
    }
}

// Create global API service instance
const apiService = new ApiService();

