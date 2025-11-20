# Install CocoaPods to Run iOS App

## ⚠️ CocoaPods Required

CocoaPods is needed for iOS development. Install it using one of these methods:

## Method 1: Using Homebrew (Recommended)

```bash
brew install cocoapods
```

## Method 2: Using RubyGems (Requires Password)

```bash
sudo gem install cocoapods
```

You'll be prompted for your password.

## Method 3: User Install (No Sudo)

```bash
gem install cocoapods --user-install
export PATH="$HOME/.gem/ruby/$(ruby -e 'puts RUBY_VERSION[/\d+\.\d+/]')/bin:$PATH"
```

## After Installation

1. **Install CocoaPods** (use one method above)

2. **Install iOS Dependencies:**
   ```bash
   cd ~/Desktop/flutter\ /mobile_app/ios
   pod install
   ```

3. **Run the App:**
   ```bash
   cd ~/Desktop/flutter\ /mobile_app
   flutter run -d "iPhone 16 Pro Max"
   ```

## Quick Install Command

If you have Homebrew:
```bash
brew install cocoapods && cd ~/Desktop/flutter\ /mobile_app/ios && pod install
```

If you prefer RubyGems (will ask for password):
```bash
sudo gem install cocoapods && cd ~/Desktop/flutter\ /mobile_app/ios && pod install
```

## Current Status

- ✅ Backend API: Running
- ✅ Simulator: Booted (iPhone 16 Pro Max)
- ✅ Flutter Code: Ready
- ❌ CocoaPods: Needs installation
- ❌ iOS Dependencies: Need pod install

## After Installing CocoaPods

Run these commands:

```bash
# 1. Install CocoaPods (choose method above)

# 2. Install iOS dependencies
cd ~/Desktop/flutter\ /mobile_app/ios
pod install

# 3. Run the app
cd ~/Desktop/flutter\ /mobile_app
flutter run -d "iPhone 16 Pro Max"
```

---

**Once CocoaPods is installed, the app will launch successfully!** 🚀

