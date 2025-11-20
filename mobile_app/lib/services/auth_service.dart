import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';
import '../models/user_model.dart';

class AuthService extends ChangeNotifier {
  final ApiService _apiService;
  User? _user;
  bool _isAuthenticated = false;
  bool _isLoading = false;

  AuthService() : _apiService = ApiService() {
    _loadAuthState();
  }

  User? get user => _user;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;

  Future<void> _loadAuthState() async {
    _isLoading = true;
    notifyListeners();

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');
      
      if (token != null) {
        _apiService.setToken(token);
        _user = await _apiService.getProfile();
        _isAuthenticated = true;
      }
    } catch (e) {
      await _clearAuthState();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  String? _lastError;
  String? get lastError => _lastError;

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _lastError = null;
    notifyListeners();

    try {
      final response = await _apiService.login(email, password);
      final token = response['access_token'] as String;
      
      await _saveAuthToken(token);
      _apiService.setToken(token);
      _user = await _apiService.getProfile();
      _isAuthenticated = true;
      
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _lastError = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> register(Map<String, dynamic> userData) async {
    _isLoading = true;
    _lastError = null;
    notifyListeners();

    try {
      final response = await _apiService.register(userData);
      final token = response['access_token'] as String;
      
      await _saveAuthToken(token);
      _apiService.setToken(token);
      _user = await _apiService.getProfile();
      _isAuthenticated = true;
      
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _lastError = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    await _clearAuthState();
    _user = null;
    _isAuthenticated = false;
    _apiService.setToken(null);
    notifyListeners();
  }

  Future<void> _saveAuthToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('auth_token', token);
  }

  Future<void> _clearAuthState() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
  }

  Future<void> updateProfile(Map<String, dynamic> userData) async {
    try {
      _user = await _apiService.updateProfile(userData);
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }
}

