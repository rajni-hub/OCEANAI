"""
Simple test script for project management endpoints
Run this after starting the server and authenticating
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token"""
    # First, try to register
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ User registered")
    except:
        pass  # User might already exist
    
    # Login
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_create_project(token):
    """Test project creation"""
    print("\n=== Testing Project Creation ===")
    url = f"{BASE_URL}/api/projects"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Test Project",
        "document_type": "word",
        "main_topic": "A market analysis of the EV industry in 2025"
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 201:
        return response.json().get("id")
    return None

def test_list_projects(token):
    """Test listing projects"""
    print("\n=== Testing List Projects ===")
    url = f"{BASE_URL}/api/projects"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_project(token, project_id):
    """Test getting a project"""
    print("\n=== Testing Get Project ===")
    url = f"{BASE_URL}/api/projects/{project_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_update_project(token, project_id):
    """Test updating a project"""
    print("\n=== Testing Update Project ===")
    url = f"{BASE_URL}/api/projects/{project_id}"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Updated Test Project",
        "main_topic": "Updated topic"
    }
    response = requests.put(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_check_exists(token, project_id):
    """Test checking if project exists"""
    print("\n=== Testing Check Project Exists ===")
    url = f"{BASE_URL}/api/projects/{project_id}/exists"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_delete_project(token, project_id):
    """Test deleting a project"""
    print("\n=== Testing Delete Project ===")
    url = f"{BASE_URL}/api/projects/{project_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print(f"Status: {response.status_code}")
    return response.status_code == 204

if __name__ == "__main__":
    print("Project Management API Test Suite")
    print("=" * 50)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ Authentication failed. Cannot proceed with tests.")
        exit(1)
    
    # Test create
    project_id = test_create_project(token)
    if project_id:
        print("✅ Project creation successful")
        
        # Test list
        if test_list_projects(token):
            print("✅ List projects successful")
        
        # Test get
        if test_get_project(token, project_id):
            print("✅ Get project successful")
        
        # Test update
        if test_update_project(token, project_id):
            print("✅ Update project successful")
        
        # Test exists check
        if test_check_exists(token, project_id):
            print("✅ Check exists successful")
        
        # Test delete
        if test_delete_project(token, project_id):
            print("✅ Delete project successful")
    else:
        print("❌ Project creation failed")
    
    print("\n" + "=" * 50)
    print("Test suite completed")

