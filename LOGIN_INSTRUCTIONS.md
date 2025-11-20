# Login Instructions

## 🔐 No Default Login Credentials

**This is a fresh application with no pre-existing users.**

You need to **register a new account first**, then you can login.

---

## 📝 How to Create an Account

### Option 1: Using the Flutter App (Recommended)

1. **Open the app** on iPhone 16 Pro Max simulator
2. **Tap "Sign Up" or "Register"** button
3. **Fill in the registration form:**
   - Email: `your-email@example.com`
   - Password: `your-password` (minimum 6 characters)
   - First Name: `Your First Name`
   - Last Name: `Your Last Name`
4. **Tap "Sign Up"**
5. **You'll be automatically logged in**

### Option 2: Using Backend API (For Testing)

1. **Open API Documentation:**
   ```
   http://localhost:8000/docs
   ```

2. **Go to `/api/v1/auth/register` endpoint**

3. **Click "Try it out"**

4. **Enter registration data:**
   ```json
   {
     "email": "test@example.com",
     "password": "test123",
     "first_name": "Test",
     "last_name": "User"
   }
   ```

5. **Click "Execute"**

6. **You'll receive an access token** - you're logged in!

---

## 🔑 After Registration

Once you've registered, you can login with:

- **Email**: The email you used to register
- **Password**: The password you set during registration

---

## 🧪 Test Credentials (Create These)

You can create test accounts with any credentials you want:

**Example Test Account:**
- Email: `test@example.com`
- Password: `test123`
- First Name: `Test`
- Last Name: `User`

**Or create your own:**
- Email: `yourname@example.com`
- Password: `yourpassword123`
- First Name: `Your Name`
- Last Name: `Your Last Name`

---

## 📱 Login in the App

1. **Open the Nutrition App** on simulator
2. **Enter your registered email**
3. **Enter your password**
4. **Tap "Sign In"**
5. **You'll be taken to the dashboard**

---

## 🌐 Login via API

1. **Open**: http://localhost:8000/docs
2. **Go to**: `/api/v1/auth/login`
3. **Enter your credentials:**
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```
4. **You'll receive an access token**

---

## ⚠️ Important Notes

- **No default users exist** - you must register first
- **Password requirements**: Minimum 6 characters
- **Email must be unique** - each email can only register once
- **After registration, you're automatically logged in**

---

## 🎯 Quick Start

1. **Register** a new account in the app
2. **Complete your profile** with health information
3. **Start using** the Nutrition App features!

---

**Register first, then login with your credentials!** 🚀

