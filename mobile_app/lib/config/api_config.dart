class ApiConfig {
  // Update this with your backend URL
  // For Android emulator, use 10.0.2.2 instead of localhost
  // For physical device, use your computer's IP address
  static const String baseUrl = 'http://10.0.2.2:8000/api/v1';
  
  // API Endpoints
  static const String login = '/auth/login';
  static const String register = '/auth/register';
  static const String profile = '/users/profile';
  static const String updateProfile = '/users/profile';
  static const String mealPlans = '/meal-plans';
  static const String meals = '/meals';
  static const String nutrition = '/nutrition/analyze';
  static const String recommendations = '/recommendations';
  static const String goals = '/goals';
  static const String progress = '/progress';
  
  // Headers
  static Map<String, String> getHeaders(String? token) {
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }
}

