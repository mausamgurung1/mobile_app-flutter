import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:io' show Platform;
import 'package:provider/provider.dart';
import '../../services/auth_service.dart';
import '../../services/tracking_service.dart';
import '../../services/api_service.dart';
import '../profile/profile_screen.dart';
import '../meal_plan/meal_plan_screen.dart';
import '../nutrition/nutrition_tracking_screen.dart';
import '../meal_plan/add_meal_screen.dart';
import '../meal_plan/generate_meal_plan_screen.dart';
import '../../widgets/nutrition_chart.dart';
import '../../widgets/water_tracker.dart';
import '../../widgets/meal_card.dart';
import '../../widgets/advanced_stats_card.dart';
import '../../widgets/macro_distribution_chart.dart';
import '../../widgets/trend_chart.dart';
import '../../models/meal_model.dart';
import 'package:intl/intl.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentIndex = 0;
  late TrackingService _trackingService;

  @override
  void initState() {
    super.initState();
    final apiService = Provider.of<ApiService>(context, listen: false);
    _trackingService = TrackingService(apiService);
  }

  @override
  Widget build(BuildContext context) {
    // Platform-specific optimizations
    final isIOS = Platform.isIOS;
    final isAndroid = Platform.isAndroid;
    
    return ChangeNotifierProvider.value(
      value: _trackingService,
      child: Scaffold(
        body: IndexedStack(
          index: _currentIndex,
          children: [
            DashboardHome(trackingService: _trackingService),
            const MealPlanScreen(),
            const NutritionTrackingScreen(),
            const ProfileScreen(),
          ],
        ),
        bottomNavigationBar: _buildBottomNavigationBar(isIOS, isAndroid),
        floatingActionButton: _buildFloatingActionButton(),
      ),
    );
  }

  Widget? _buildFloatingActionButton() {
    if (_currentIndex == 0) {
      // Home tab - Log Meal button
      return FloatingActionButton.extended(
        heroTag: "fab_home",
        onPressed: () {
          HapticFeedback.mediumImpact();
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => const AddMealScreen(),
            ),
          );
        },
        icon: const Icon(Icons.add),
        label: const Text('Log Meal'),
        elevation: 4,
      );
    } else if (_currentIndex == 1) {
      // Meal Plans tab - Generate Plan button
      return FloatingActionButton.extended(
        heroTag: "fab_meal_plan",
        onPressed: () {
          HapticFeedback.mediumImpact();
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => const GenerateMealPlanScreen(),
            ),
          );
        },
        icon: const Icon(Icons.auto_awesome),
        label: const Text('Generate Plan'),
      );
    }
    return null;
  }

  Widget _buildBottomNavigationBar(bool isIOS, bool isAndroid) {
    if (isIOS) {
      // iOS-style navigation with CupertinoTabBar
      return NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          HapticFeedback.selectionClick();
          setState(() {
            _currentIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.dashboard_outlined),
            selectedIcon: Icon(Icons.dashboard),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.restaurant_menu_outlined),
            selectedIcon: Icon(Icons.restaurant_menu),
            label: 'Meals',
          ),
          NavigationDestination(
            icon: Icon(Icons.track_changes_outlined),
            selectedIcon: Icon(Icons.track_changes),
            label: 'Nutrition',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      );
    } else {
      // Android-style navigation
      return NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          HapticFeedback.mediumImpact();
          setState(() {
            _currentIndex = index;
          });
        },
        height: 70,
        labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.dashboard_outlined),
            selectedIcon: Icon(Icons.dashboard),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.restaurant_menu_outlined),
            selectedIcon: Icon(Icons.restaurant_menu),
            label: 'Meals',
          ),
          NavigationDestination(
            icon: Icon(Icons.track_changes_outlined),
            selectedIcon: Icon(Icons.track_changes),
            label: 'Nutrition',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      );
    }
  }
}

class DashboardHome extends StatefulWidget {
  final TrackingService trackingService;

  const DashboardHome({super.key, required this.trackingService});

  @override
  State<DashboardHome> createState() => _DashboardHomeState();
}

class _DashboardHomeState extends State<DashboardHome> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final authService = Provider.of<AuthService>(context, listen: false);
      if (authService.isAuthenticated) {
        widget.trackingService.loadTodayMeals();
        widget.trackingService.loadWeeklyNutrition();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final authService = Provider.of<AuthService>(context);
    final user = authService.user;
    final trackingService = widget.trackingService;
    final targetNutrition = trackingService.getTargetNutrition(user);
    final isIOS = Platform.isIOS;

    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        systemOverlayStyle: isIOS 
          ? SystemUiOverlayStyle.dark 
          : SystemUiOverlayStyle.light,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Hello, ${user?.firstName ?? 'User'}! 👋',
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              DateFormat('EEEE, MMMM d').format(DateTime.now()),
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {
              HapticFeedback.mediumImpact();
              // TODO: Implement notifications
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          HapticFeedback.mediumImpact();
          final authService = Provider.of<AuthService>(context, listen: false);
          if (authService.isAuthenticated) {
            await trackingService.loadTodayMeals();
            await trackingService.loadWeeklyNutrition();
          }
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Advanced Stats Card
              ChangeNotifierProvider.value(
                value: trackingService,
                child: Consumer<TrackingService>(
                  builder: (context, service, _) {
                    return AdvancedStatsCard(
                      user: user,
                      todayNutrition: service.todayNutrition,
                      targetNutrition: targetNutrition,
                    );
                  },
                ),
              ),
              const SizedBox(height: 16),

              // Water Tracker
              ChangeNotifierProvider.value(
                value: trackingService,
                child: Consumer<TrackingService>(
                  builder: (context, service, _) {
                    return WaterTracker(
                      current: service.waterIntake,
                      target: service.getWaterTarget(),
                      onAdd: (amount) {
                        HapticFeedback.lightImpact();
                        service.addWater(amount);
                      },
                    );
                  },
                ),
              ),
              const SizedBox(height: 16),

              // Macro Distribution Chart
              ChangeNotifierProvider.value(
                value: trackingService,
                child: Consumer<TrackingService>(
                  builder: (context, service, _) {
                    return MacroDistributionChart(
                      current: service.todayNutrition,
                      target: targetNutrition,
                    );
                  },
                ),
              ),
              const SizedBox(height: 16),

              // Nutrition Progress
              _buildNutritionProgress(trackingService, targetNutrition),
              const SizedBox(height: 16),

              // Weekly Trend Charts
              if (trackingService.weeklyNutrition.isNotEmpty) ...[
                _buildTrendCharts(trackingService),
                const SizedBox(height: 16),
              ],

              // Today's Meals
              _buildTodaysMeals(trackingService),
              const SizedBox(height: 16),

              // Quick Actions
              _buildQuickActions(context),
              const SizedBox(height: 80), // Space for FAB
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTrendCharts(TrackingService service) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Weekly Trends',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        TrendChart(
          weeklyData: service.weeklyNutrition,
          metric: 'calories',
          color: Colors.orange,
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: TrendChart(
                weeklyData: service.weeklyNutrition,
                metric: 'protein',
                color: Colors.blue,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: TrendChart(
                weeklyData: service.weeklyNutrition,
                metric: 'carbs',
                color: Colors.green,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildNutritionProgress(TrackingService service, NutritionInfo? target) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Nutrition Progress',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        NutritionChart(
          current: service.todayNutrition,
          target: target,
          nutrient: 'protein',
          color: Colors.blue,
        ),
        const SizedBox(height: 12),
        NutritionChart(
          current: service.todayNutrition,
          target: target,
          nutrient: 'carbs',
          color: Colors.green,
        ),
        const SizedBox(height: 12),
        NutritionChart(
          current: service.todayNutrition,
          target: target,
          nutrient: 'fat',
          color: Colors.purple,
        ),
      ],
    );
  }

  Widget _buildTodaysMeals(TrackingService service) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              "Today's Meals",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const AddMealScreen(),
                  ),
                );
              },
              child: const Text('Add Meal'),
            ),
          ],
        ),
        const SizedBox(height: 12),
        ChangeNotifierProvider.value(
          value: service,
          child: Consumer<TrackingService>(
            builder: (context, service, _) {
              if (service.isLoading) {
                return const Center(
                  child: Padding(
                    padding: EdgeInsets.all(32.0),
                    child: CircularProgressIndicator(),
                  ),
                );
              }

              final meals = service.todayMeals;
              if (meals.isEmpty) {
                return _buildEmptyMealsState();
              }

              return Column(
                children: meals.map((meal) {
                  return MealCard(
                    meal: meal,
                    onTap: () {
                      // TODO: Show meal details
                    },
                  );
                }).toList(),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildEmptyMealsState() {
    return Container(
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        children: [
          Icon(
            Icons.restaurant_menu,
            size: 64,
            color: Colors.grey[400],
          ),
          const SizedBox(height: 16),
          Text(
            'No meals logged today',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey[600],
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Tap the button below to log your first meal',
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey[500],
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildQuickActions(BuildContext context) {
    final authService = Provider.of<AuthService>(context);
    final user = authService.user;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Quick Actions',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildActionCard(
                context,
                icon: Icons.auto_awesome,
                title: 'Get Recommendations',
                color: Colors.purple,
                onTap: () {
                  // TODO: Navigate to recommendations
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Recommendations coming soon!'),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildActionCard(
                context,
                icon: Icons.calendar_today,
                title: 'Meal Plan',
                color: Colors.green,
                onTap: () {
                  // TODO: Navigate to meal plan
                },
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildActionCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(height: 8),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w500,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
