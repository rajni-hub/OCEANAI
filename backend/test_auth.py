"""
Simple test script for authentication endpoints
Run this after starting the server to test authentication
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    url = f"{BASE_URL}/api/auth/login"
    # Using form data (OAuth2PasswordRequestForm)
    data = {
        "username": "test@example.com",  # OAuth2 uses 'username' for email
        "password": "testpassword123"
    }
    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    return None

def test_login_json():
    """Test user login with JSON"""
    print("\n=== Testing User Login (JSON) ===")
    url = f"{BASE_URL}/api/auth/login-json"
    data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    return None

def test_me(token):
    """Test getting current user info"""
    print("\n=== Testing Get Current User ===")
    url = f"{BASE_URL}/api/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_verify_token(token):
    """Test token verification"""
    print("\n=== Testing Token Verification ===")
    url = f"{BASE_URL}/api/auth/verify-token"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_refresh_token(token):
    """Test token refresh"""
    print("\n=== Testing Token Refresh ===")
    url = f"{BASE_URL}/api/auth/refresh"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Authentication API Test Suite")
    print("=" * 50)
    
    # Test registration
    if test_register():
        print("✅ Registration successful")
    else:
        print("❌ Registration failed")
    
    # Test login
    token = test_login()
    if token:
        print("✅ Login successful")
        
        # Test protected endpoints
        if test_me(token):
            print("✅ Get current user successful")
        
        if test_verify_token(token):
            print("✅ Token verification successful")
        
        if test_refresh_token(token):
            print("✅ Token refresh successful")
    else:
        print("❌ Login failed")
    
    print("\n" + "=" * 50)
    print("Test suite completed")

