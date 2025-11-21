// Dashboard page functionality

let userProfile = null;
let todayMeals = [];
let todayNutrition = {
    calories: 0,
    protein: 0,
    carbohydrates: 0,
    fat: 0,
    fiber: 0
};

// Load dashboard data
async function loadDashboard() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.style.display = 'flex';
    
    try {
        // Load user profile
        userProfile = await apiService.getProfile();
        displayProfile();
        
        // Load today's meal plans
        await loadTodayMeals();
        
        // Calculate and display nutrition
        calculateTodayNutrition();
        displayNutrition();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        if (error.message.includes('401') || error.message.includes('credentials')) {
            logout();
        }
    } finally {
        loadingOverlay.style.display = 'none';
    }
}

// Display user profile
function displayProfile() {
    if (!userProfile) return;
    
    document.getElementById('userName').textContent = 
        `${userProfile.first_name || ''} ${userProfile.last_name || ''}`.trim() || 'User';
    
    document.getElementById('userGoal').textContent = 
        formatHealthGoal(userProfile.health_goal);
    document.getElementById('userAge').textContent = userProfile.age || '-';
    document.getElementById('userHeight').textContent = userProfile.height || '-';
    document.getElementById('userWeight').textContent = userProfile.weight || '-';
    document.getElementById('userActivity').textContent = 
        formatActivityLevel(userProfile.activity_level);
}

// Load today's meals from meal plans
async function loadTodayMeals() {
    const now = new Date();
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const endOfDay = new Date(startOfDay);
    endOfDay.setDate(endOfDay.getDate() + 1);
    
    try {
        const mealPlans = await apiService.getMealPlans(startOfDay, endOfDay);
        
        todayMeals = [];
        mealPlans.forEach(plan => {
            if (plan.meals && Array.isArray(plan.meals)) {
                plan.meals.forEach(meal => {
                    const mealDate = new Date(meal.date);
                    if (mealDate >= startOfDay && mealDate < endOfDay) {
                        todayMeals.push(meal);
                    }
                });
            }
        });
        
        displayTodayMeals();
    } catch (error) {
        console.error('Error loading today meals:', error);
    }
}

// Display today's meals
function displayTodayMeals() {
    const container = document.getElementById('todayMeals');
    
    if (todayMeals.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No meals logged today</p>
                <button class="btn btn-primary" onclick="window.location.href='/meal-plans.html'">
                    Generate Meal Plan
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = todayMeals.map(meal => `
        <div class="meal-item">
            <div class="meal-header">
                <span class="meal-name">${meal.name || 'Meal'}</span>
                <span class="meal-type">${meal.meal_type || 'meal'}</span>
            </div>
            ${meal.description ? `<p style="color: var(--text-secondary); font-size: 0.9rem; margin: 8px 0;">${meal.description}</p>` : ''}
            ${meal.foods && meal.foods.length > 0 ? `
                <div class="meal-foods">
                    ${meal.foods.map(food => `${food.name} (${food.quantity} ${food.unit})`).join(', ')}
                </div>
            ` : ''}
            ${meal.nutrition ? `
                <div style="margin-top: 8px; font-size: 0.85rem; color: var(--text-secondary);">
                    ${Math.round(meal.nutrition.calories || 0)} cal | 
                    ${Math.round(meal.nutrition.protein || 0)}g protein | 
                    ${Math.round(meal.nutrition.carbohydrates || 0)}g carbs
                </div>
            ` : ''}
        </div>
    `).join('');
}

// Calculate today's nutrition totals
function calculateTodayNutrition() {
    todayNutrition = {
        calories: 0,
        protein: 0,
        carbohydrates: 0,
        fat: 0,
        fiber: 0
    };
    
    todayMeals.forEach(meal => {
        if (meal.nutrition) {
            todayNutrition.calories += meal.nutrition.calories || 0;
            todayNutrition.protein += meal.nutrition.protein || 0;
            todayNutrition.carbohydrates += meal.nutrition.carbohydrates || 0;
            todayNutrition.fat += meal.nutrition.fat || 0;
            todayNutrition.fiber += meal.nutrition.fiber || 0;
        }
    });
}

// Display nutrition stats
function displayNutrition() {
    // Set targets (you can calculate these based on user profile)
    const targets = {
        calories: 2000,
        protein: 150,
        carbohydrates: 250,
        fat: 65
    };
    
    // Update values
    document.getElementById('calories').textContent = Math.round(todayNutrition.calories);
    document.getElementById('caloriesTarget').textContent = targets.calories;
    document.getElementById('protein').textContent = Math.round(todayNutrition.protein);
    document.getElementById('proteinTarget').textContent = targets.protein;
    document.getElementById('carbs').textContent = Math.round(todayNutrition.carbohydrates);
    document.getElementById('carbsTarget').textContent = targets.carbohydrates;
    document.getElementById('fat').textContent = Math.round(todayNutrition.fat);
    document.getElementById('fatTarget').textContent = targets.fat;
    
    // Update progress bars
    updateProgressBar('caloriesProgress', todayNutrition.calories, targets.calories);
    updateProgressBar('proteinProgress', todayNutrition.protein, targets.protein);
    updateProgressBar('carbsProgress', todayNutrition.carbohydrates, targets.carbohydrates);
    updateProgressBar('fatProgress', todayNutrition.fat, targets.fat);
}

// Update progress bar
function updateProgressBar(elementId, current, target) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const percentage = Math.min((current / target) * 100, 100);
    element.style.width = `${percentage}%`;
}

// Format health goal
function formatHealthGoal(goal) {
    if (!goal) return '-';
    return goal.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Format activity level
function formatActivityLevel(level) {
    if (!level) return '-';
    return level.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Initialize dashboard on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadDashboard);
} else {
    loadDashboard();
}

