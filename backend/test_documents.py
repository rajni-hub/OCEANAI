"""
Simple test script for document configuration endpoints
Run this after starting the server and authenticating
"""
import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token"""
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    except:
        pass
    
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def create_project(token, doc_type="word"):
    """Create a test project"""
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": f"Test {doc_type.title()} Project",
        "document_type": doc_type,
        "main_topic": "A market analysis of the EV industry in 2025"
    }
    response = requests.post(f"{BASE_URL}/api/projects", json=data, headers=headers)
    if response.status_code == 201:
        return response.json().get("id")
    return None

def test_configure_word_document(token, project_id):
    """Test Word document configuration"""
    print("\n=== Testing Word Document Configuration ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "structure": {
            "sections": [
                {"id": "section-1", "title": "Introduction", "order": 0},
                {"id": "section-2", "title": "Background", "order": 1},
                {"id": "section-3", "title": "Analysis", "order": 2},
                {"id": "section-4", "title": "Conclusion", "order": 3}
            ]
        }
    }
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/configure",
        json=data,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_configure_powerpoint_document(token, project_id):
    """Test PowerPoint document configuration"""
    print("\n=== Testing PowerPoint Document Configuration ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "structure": {
            "slides": [
                {"id": "slide-1", "title": "Title Slide", "order": 0},
                {"id": "slide-2", "title": "Overview", "order": 1},
                {"id": "slide-3", "title": "Key Points", "order": 2},
                {"id": "slide-4", "title": "Conclusion", "order": 3}
            ]
        }
    }
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/configure",
        json=data,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_document(token, project_id):
    """Test getting document"""
    print("\n=== Testing Get Document ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}/document",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_update_structure(token, project_id, doc_type="word"):
    """Test updating document structure"""
    print("\n=== Testing Update Document Structure ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    if doc_type == "word":
        data = {
            "structure": {
                "sections": [
                    {"id": "section-1", "title": "Updated Introduction", "order": 0},
                    {"id": "section-2", "title": "Updated Background", "order": 1}
                ]
            }
        }
    else:
        data = {
            "structure": {
                "slides": [
                    {"id": "slide-1", "title": "Updated Title", "order": 0},
                    {"id": "slide-2", "title": "Updated Overview", "order": 1}
                ]
            }
        }
    
    response = requests.put(
        f"{BASE_URL}/api/projects/{project_id}/document/structure",
        json=data,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_reorder_sections(token, project_id):
    """Test reordering sections"""
    print("\n=== Testing Reorder Sections ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "section-2": 0,
        "section-1": 1
    }
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/document/reorder-sections",
        json=data,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_ai_template(token, project_id, doc_type="word"):
    """Test AI template generation (Bonus)"""
    print("\n=== Testing AI Template Generation (Bonus) ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "main_topic": "A market analysis of the EV industry in 2025",
        "document_type": doc_type
    }
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/generate-template",
        json=data,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    print("Document Configuration API Test Suite")
    print("=" * 50)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ Authentication failed. Cannot proceed with tests.")
        exit(1)
    
    # Test Word document
    print("\n" + "=" * 50)
    print("Testing Word Document Configuration")
    print("=" * 50)
    
    word_project_id = create_project(token, "word")
    if word_project_id:
        print(f"✅ Word project created: {word_project_id}")
        
        if test_configure_word_document(token, word_project_id):
            print("✅ Word document configuration successful")
        
        if test_get_document(token, word_project_id):
            print("✅ Get document successful")
        
        if test_update_structure(token, word_project_id, "word"):
            print("✅ Update structure successful")
        
        if test_reorder_sections(token, word_project_id):
            print("✅ Reorder sections successful")
        
        if test_ai_template(token, word_project_id, "word"):
            print("✅ AI template generation successful")
    
    # Test PowerPoint document
    print("\n" + "=" * 50)
    print("Testing PowerPoint Document Configuration")
    print("=" * 50)
    
    ppt_project_id = create_project(token, "powerpoint")
    if ppt_project_id:
        print(f"✅ PowerPoint project created: {ppt_project_id}")
        
        if test_configure_powerpoint_document(token, ppt_project_id):
            print("✅ PowerPoint document configuration successful")
        
        if test_get_document(token, ppt_project_id):
            print("✅ Get document successful")
        
        if test_update_structure(token, ppt_project_id, "powerpoint"):
            print("✅ Update structure successful")
        
        if test_ai_template(token, ppt_project_id, "powerpoint"):
            print("✅ AI template generation successful")
    
    print("\n" + "=" * 50)
    print("Test suite completed")

