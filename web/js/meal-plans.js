// Meal Plans page functionality

let mealPlans = [];

// Load meal plans
async function loadMealPlans() {
    const container = document.getElementById('mealPlansContainer');
    container.innerHTML = `
        <div class="loading-state">
            <div class="spinner-large"></div>
            <p>Loading meal plans...</p>
        </div>
    `;
    
    try {
        mealPlans = await apiService.getMealPlans();
        displayMealPlans();
    } catch (error) {
        console.error('Error loading meal plans:', error);
        container.innerHTML = `
            <div class="empty-state">
                <p>Error loading meal plans: ${error.message}</p>
                <button class="btn btn-primary" onclick="loadMealPlans()">Retry</button>
            </div>
        `;
    }
}

// Display meal plans
function displayMealPlans() {
    const container = document.getElementById('mealPlansContainer');
    
    if (mealPlans.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No meal plans yet. Generate your first meal plan to get started!</p>
                <button class="btn btn-primary" id="emptyGenerateBtn">Generate Meal Plan</button>
            </div>
        `;
        // Add event listener to the button
        setTimeout(() => {
            const btn = document.getElementById('emptyGenerateBtn');
            if (btn) {
                btn.addEventListener('click', openGenerateModal);
            }
        }, 100);
        return;
    }
    
    container.innerHTML = mealPlans.map(plan => {
        const startDate = new Date(plan.start_date);
        const endDate = new Date(plan.end_date);
        const meals = plan.meals || [];
        
        return `
            <div class="meal-plan-card">
                <div class="meal-plan-header">
                    <h3>Meal Plan</h3>
                    <div class="meal-plan-dates">
                        ${formatDate(startDate)} - ${formatDate(endDate)}
                    </div>
                </div>
                <div class="meal-plan-body">
                    <span class="meal-plan-goal">${formatGoal(plan.goal)}</span>
                    ${plan.daily_nutrition ? `
                        <div style="margin-bottom: 15px; padding: 10px; background: var(--bg-secondary); border-radius: 6px;">
                            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 5px;">Daily Targets:</div>
                            <div style="font-size: 0.9rem;">
                                ${Math.round(plan.daily_nutrition.calories || 0)} cal | 
                                ${Math.round(plan.daily_nutrition.protein || 0)}g protein | 
                                ${Math.round(plan.daily_nutrition.carbohydrates || 0)}g carbs | 
                                ${Math.round(plan.daily_nutrition.fat || 0)}g fat
                            </div>
                        </div>
                    ` : ''}
                    <div class="meal-plan-meals">
                        ${meals.length > 0 ? `
                            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 10px;">
                                ${meals.length} meal${meals.length !== 1 ? 's' : ''} planned
                            </div>
                            ${meals.slice(0, 5).map(meal => `
                                <div class="meal-plan-meal">
                                    <strong>${meal.name || 'Meal'}</strong> 
                                    <span style="color: var(--text-secondary);">(${meal.meal_type})</span>
                                    ${meal.nutrition ? `
                                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;">
                                            ${Math.round(meal.nutrition.calories || 0)} cal
                                        </div>
                                    ` : ''}
                                </div>
                            `).join('')}
                            ${meals.length > 5 ? `
                                <div style="text-align: center; margin-top: 10px; color: var(--text-secondary); font-size: 0.85rem;">
                                    +${meals.length - 5} more meals
                                </div>
                            ` : ''}
                        ` : `
                            <div style="text-align: center; padding: 20px; color: var(--text-secondary);">
                                No meals in this plan yet
                            </div>
                        `}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Format date
function formatDate(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// Format goal
function formatGoal(goal) {
    if (!goal) return 'Maintenance';
    return goal.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Open generate modal
function openGenerateModal() {
    const modal = document.getElementById('generateModal');
    const today = new Date();
    const nextWeek = new Date(today);
    nextWeek.setDate(nextWeek.getDate() + 7);
    
    document.getElementById('startDate').value = today.toISOString().split('T')[0];
    document.getElementById('endDate').value = nextWeek.toISOString().split('T')[0];
    modal.style.display = 'flex';
}

// Close generate modal
function closeGenerateModal() {
    const modal = document.getElementById('generateModal');
    modal.style.display = 'none';
    document.getElementById('generateError').classList.remove('show');
    document.getElementById('generateForm').reset();
}

// Generate meal plan
async function generateMealPlan(e) {
    e.preventDefault();
    
    const errorDiv = document.getElementById('generateError');
    errorDiv.classList.remove('show');
    
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);
    const goal = document.getElementById('goal').value || null;
    
    // Validate dates
    if (endDate <= startDate) {
        errorDiv.textContent = 'End date must be after start date';
        errorDiv.classList.add('show');
        return;
    }
    
    const daysDiff = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
    if (daysDiff > 30) {
        errorDiv.textContent = 'Meal plan cannot exceed 30 days';
        errorDiv.classList.add('show');
        return;
    }
    
    // Show loading state
    const generateBtnText = document.getElementById('generateBtnText');
    const generateBtnSpinner = document.getElementById('generateBtnSpinner');
    generateBtnText.style.display = 'none';
    generateBtnSpinner.style.display = 'inline-block';
    e.target.querySelector('button[type="submit"]').disabled = true;
    
    try {
        await apiService.generateMealPlan(startDate, endDate, goal);
        closeGenerateModal();
        loadMealPlans();
    } catch (error) {
        errorDiv.textContent = error.message || 'Failed to generate meal plan';
        errorDiv.classList.add('show');
    } finally {
        generateBtnText.style.display = 'inline';
        generateBtnSpinner.style.display = 'none';
        e.target.querySelector('button[type="submit"]').disabled = false;
    }
}

// Event listeners
document.getElementById('generateMealPlanBtn').addEventListener('click', openGenerateModal);
document.getElementById('refreshBtn').addEventListener('click', loadMealPlans);
document.getElementById('closeModal').addEventListener('click', closeGenerateModal);
document.getElementById('cancelGenerate').addEventListener('click', closeGenerateModal);
document.getElementById('generateForm').addEventListener('submit', generateMealPlan);

// Close modal when clicking outside
document.getElementById('generateModal').addEventListener('click', (e) => {
    if (e.target.id === 'generateModal') {
        closeGenerateModal();
    }
});

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadMealPlans);
} else {
    loadMealPlans();
}

