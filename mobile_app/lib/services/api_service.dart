import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/user_model.dart';
import '../models/meal_model.dart';
import '../models/meal_plan_model.dart';

class ApiService extends ChangeNotifier {
  String? _token;
  User? _currentUser;

  String? get token => _token;
  User? get currentUser => _currentUser;

  void setToken(String? token) {
    _token = token;
    notifyListeners();
  }

  void setUser(User? user) {
    _currentUser = user;
    notifyListeners();
  }

  Future<dynamic> _request(
    String method,
    String endpoint, {
    Map<String, dynamic>? body,
  }) async {
    final url = Uri.parse('${ApiConfig.baseUrl}$endpoint');
    final headers = ApiConfig.getHeaders(_token);

    http.Response response;

    switch (method.toUpperCase()) {
      case 'GET':
        response = await http.get(url, headers: headers);
        break;
      case 'POST':
        response = await http.post(
          url,
          headers: headers,
          body: body != null ? jsonEncode(body) : null,
        );
        break;
      case 'PUT':
        response = await http.put(
          url,
          headers: headers,
          body: body != null ? jsonEncode(body) : null,
        );
        break;
      case 'DELETE':
        response = await http.delete(url, headers: headers);
        break;
      default:
        throw Exception('Unsupported HTTP method');
    }

    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) {
        return {};
      }
      final decoded = jsonDecode(response.body);
      // Handle both list and map responses from FastAPI
      return decoded;
    } else {
      String errorMessage = 'Request failed';
      try {
        final error = jsonDecode(response.body) as Map<String, dynamic>;
        errorMessage = error['detail'] ?? error['message'] ?? errorMessage;
      } catch (e) {
        errorMessage = response.body.isNotEmpty ? response.body : 'Request failed with status ${response.statusCode}';
      }
      throw Exception(errorMessage);
    }
  }

  // Auth endpoints
  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await _request('POST', ApiConfig.login, body: {
      'email': email,
      'password': password,
    });
    return response;
  }

  Future<Map<String, dynamic>> register(Map<String, dynamic> userData) async {
    final response = await _request('POST', ApiConfig.register, body: userData);
    return response;
  }

  // User endpoints
  Future<User> getProfile() async {
    final response = await _request('GET', ApiConfig.profile);
    return User.fromJson(response as Map<String, dynamic>);
  }

  Future<User> updateProfile(Map<String, dynamic> userData) async {
    final response = await _request('PUT', ApiConfig.updateProfile, body: userData);
    return User.fromJson(response as Map<String, dynamic>);
  }

  // Meal Plan endpoints
  Future<List<MealPlan>> getMealPlans({DateTime? startDate, DateTime? endDate}) async {
    String endpoint = ApiConfig.mealPlans;
    if (startDate != null && endDate != null) {
      endpoint += '?start_date=${startDate.toIso8601String()}&end_date=${endDate.toIso8601String()}';
    }
    final response = await _request('GET', endpoint);
    // Response is a list directly from FastAPI
    if (response is List) {
      return (response as List<dynamic>).map((m) => MealPlan.fromJson(m as Map<String, dynamic>)).toList();
    }
    // Fallback if wrapped (shouldn't happen with FastAPI but just in case)
    final List<dynamic> data = (response as Map<String, dynamic>)['data'] as List<dynamic>? ?? [];
    return data.map((m) => MealPlan.fromJson(m as Map<String, dynamic>)).toList();
  }

  Future<MealPlan> createMealPlan(Map<String, dynamic> mealPlanData) async {
    final response = await _request('POST', ApiConfig.mealPlans, body: mealPlanData);
    if (response is Map<String, dynamic>) {
      return MealPlan.fromJson(response);
    }
    return MealPlan.fromJson((response as Map<String, dynamic>)['data'] as Map<String, dynamic>);
  }

  // Generate meal plan automatically
  Future<MealPlan> generateMealPlan({
    required DateTime startDate,
    required DateTime endDate,
    String? goal,
  }) async {
    String endpoint = '${ApiConfig.mealPlans}/generate?start_date=${startDate.toIso8601String()}&end_date=${endDate.toIso8601String()}';
    if (goal != null) {
      endpoint += '&goal=$goal';
    }
    final response = await _request('POST', endpoint);
    if (response is Map<String, dynamic>) {
      return MealPlan.fromJson(response);
    }
    return MealPlan.fromJson((response as Map<String, dynamic>)['data'] as Map<String, dynamic>);
  }

  // Nutrition analysis
  Future<NutritionInfo> analyzeNutrition(List<FoodItem> foods) async {
    final response = await _request('POST', ApiConfig.nutrition, body: {
      'foods': foods.map((f) => f.toJson()).toList(),
    });
    if (response is Map<String, dynamic>) {
      return NutritionInfo.fromJson(response);
    }
    return NutritionInfo.fromJson((response as Map<String, dynamic>)['data'] as Map<String, dynamic>);
  }

  // Recommendations
  Future<List<Meal>> getRecommendations({
    required String mealType,
    DateTime? date,
  }) async {
    String endpoint = '${ApiConfig.recommendations}?meal_type=$mealType';
    if (date != null) {
      endpoint += '&date=${date.toIso8601String()}';
    }
    final response = await _request('GET', endpoint);
    // Response is a list directly from FastAPI
    if (response is List) {
      return (response as List<dynamic>).map((m) => Meal.fromJson(m as Map<String, dynamic>)).toList();
    }
    // Fallback if wrapped (shouldn't happen with FastAPI but just in case)
    final List<dynamic> data = (response as Map<String, dynamic>)['data'] as List<dynamic>? ?? [];
    return data.map((m) => Meal.fromJson(m as Map<String, dynamic>)).toList();
  }
}

