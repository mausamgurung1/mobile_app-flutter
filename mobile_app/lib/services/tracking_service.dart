import 'package:flutter/foundation.dart';
import '../models/meal_model.dart';
import '../models/user_model.dart';
import 'api_service.dart';

class TrackingService extends ChangeNotifier {
  final ApiService _apiService;
  
  List<Meal> _todayMeals = [];
  NutritionInfo? _todayNutrition;
  double _waterIntake = 0.0; // in ml
  Map<DateTime, NutritionInfo> _weeklyNutrition = {};
  bool _isLoading = false;

  TrackingService(this._apiService);

  List<Meal> get todayMeals => _todayMeals;
  NutritionInfo? get todayNutrition => _todayNutrition;
  double get waterIntake => _waterIntake;
  Map<DateTime, NutritionInfo> get weeklyNutrition => _weeklyNutrition;
  bool get isLoading => _isLoading;

  // Calculate daily nutrition from meals
  NutritionInfo _calculateDailyNutrition(List<Meal> meals) {
    double calories = 0;
    double protein = 0;
    double carbs = 0;
    double fat = 0;
    double fiber = 0;

    for (var meal in meals) {
      if (meal.nutrition != null) {
        calories += meal.nutrition!.calories;
        protein += meal.nutrition!.protein;
        carbs += meal.nutrition!.carbohydrates;
        fat += meal.nutrition!.fat;
        fiber += meal.nutrition!.fiber;
      }
    }

    return NutritionInfo(
      calories: calories,
      protein: protein,
      carbohydrates: carbs,
      fat: fat,
      fiber: fiber,
    );
  }

  // Get target nutrition based on user profile
  NutritionInfo? getTargetNutrition(User? user) {
    if (user == null) return null;
    
    final tdee = _calculateTDEE(user);
    if (tdee == null) return null;

    // Calculate macros based on goal
    double proteinRatio = 0.25; // 25% protein
    double carbRatio = 0.45; // 45% carbs
    double fatRatio = 0.30; // 30% fat

    if (user.healthGoal == 'weight_loss') {
      // Slightly higher protein for weight loss
      proteinRatio = 0.30;
      carbRatio = 0.40;
      fatRatio = 0.30;
    } else if (user.healthGoal == 'muscle_gain') {
      // Higher protein and carbs for muscle gain
      proteinRatio = 0.30;
      carbRatio = 0.50;
      fatRatio = 0.20;
    }

    return NutritionInfo(
      calories: tdee,
      protein: (tdee * proteinRatio) / 4, // 4 calories per gram
      carbohydrates: (tdee * carbRatio) / 4, // 4 calories per gram
      fat: (tdee * fatRatio) / 9, // 9 calories per gram
      fiber: 25.0, // Recommended daily fiber
    );
  }

  double? _calculateTDEE(User user) {
    if (user.age == null || user.height == null || user.weight == null || user.gender == null) {
      return null;
    }

    // BMR calculation (Mifflin-St Jeor)
    double bmr;
    if (user.gender!.toLowerCase() == 'male') {
      bmr = 10 * user.weight! + 6.25 * user.height! - 5 * user.age! + 5;
    } else {
      bmr = 10 * user.weight! + 6.25 * user.height! - 5 * user.age! - 161;
    }

    // Activity multipliers
    final multipliers = {
      'sedentary': 1.2,
      'lightly_active': 1.375,
      'moderately_active': 1.55,
      'very_active': 1.725,
      'extremely_active': 1.9,
    };

    final multiplier = multipliers[user.activityLevel] ?? 1.2;
    return bmr * multiplier;
  }

  Future<void> loadTodayMeals() async {
    _isLoading = true;
    notifyListeners();

    try {
      final now = DateTime.now();
      final startOfDay = DateTime(now.year, now.month, now.day);
      final endOfDay = startOfDay.add(const Duration(days: 1));

      final mealPlans = await _apiService.getMealPlans(
        startDate: startOfDay,
        endDate: endOfDay,
      );

      _todayMeals = [];
      for (var plan in mealPlans) {
        _todayMeals.addAll(plan.meals.where((m) {
          final mealDate = m.date is DateTime ? m.date as DateTime : DateTime.parse(m.date.toString());
          return mealDate.isAfter(startOfDay) && mealDate.isBefore(endOfDay);
        }));
      }

      _todayNutrition = _calculateDailyNutrition(_todayMeals);
    } catch (e) {
      debugPrint('Error loading today meals: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadWeeklyNutrition() async {
    try {
      final now = DateTime.now();
      final startOfWeek = now.subtract(Duration(days: now.weekday - 1));
      
      _weeklyNutrition = {};
      
      for (int i = 0; i < 7; i++) {
        final date = startOfWeek.add(Duration(days: i));
        final startOfDay = DateTime(date.year, date.month, date.day);
        final endOfDay = startOfDay.add(const Duration(days: 1));

        final mealPlans = await _apiService.getMealPlans(
          startDate: startOfDay,
          endDate: endOfDay,
        );

        List<Meal> dayMeals = [];
        for (var plan in mealPlans) {
          dayMeals.addAll(plan.meals.where((m) {
            final mealDate = m.date is DateTime ? m.date as DateTime : DateTime.parse(m.date.toString());
            return mealDate.isAfter(startOfDay) && mealDate.isBefore(endOfDay);
          }));
        }

        _weeklyNutrition[date] = _calculateDailyNutrition(dayMeals);
      }
      
      notifyListeners();
    } catch (e) {
      debugPrint('Error loading weekly nutrition: $e');
    }
  }

  void addWater(double amount) {
    _waterIntake += amount;
    notifyListeners();
  }

  void resetWater() {
    _waterIntake = 0.0;
    notifyListeners();
  }

  double getWaterTarget() {
    return 2000.0; // 2 liters default
  }

  double getWaterProgress() {
    return _waterIntake / getWaterTarget();
  }

  List<Meal> getMealsByType(String mealType) {
    return _todayMeals.where((m) => m.mealType == mealType).toList();
  }

  double getProgressPercentage(NutritionInfo? target, NutritionInfo? current, String nutrient) {
    if (target == null || current == null) return 0.0;
    
    double targetValue = 0;
    double currentValue = 0;
    
    switch (nutrient) {
      case 'calories':
        targetValue = target.calories;
        currentValue = current.calories;
        break;
      case 'protein':
        targetValue = target.protein;
        currentValue = current.protein;
        break;
      case 'carbs':
        targetValue = target.carbohydrates;
        currentValue = current.carbohydrates;
        break;
      case 'fat':
        targetValue = target.fat;
        currentValue = current.fat;
        break;
    }
    
    if (targetValue == 0) return 0.0;
    return (currentValue / targetValue).clamp(0.0, 1.5); // Allow up to 150% for visualization
  }
}

