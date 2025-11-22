"""
Simple test script for content generation endpoints
Run this after starting the server and authenticating
"""
import requests
import json
import time

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

def create_and_configure_project(token, doc_type="word"):
    """Create and configure a test project"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create project
    project_data = {
        "title": f"Test {doc_type.title()} Project",
        "document_type": doc_type,
        "main_topic": "A market analysis of the EV industry in 2025"
    }
    response = requests.post(f"{BASE_URL}/api/projects", json=project_data, headers=headers)
    if response.status_code != 201:
        print(f"Failed to create project: {response.text}")
        return None
    
    project_id = response.json().get("id")
    
    # Configure document structure
    if doc_type == "word":
        structure = {
            "structure": {
                "sections": [
                    {"id": "section-1", "title": "Introduction", "order": 0},
                    {"id": "section-2", "title": "Background", "order": 1},
                    {"id": "section-3", "title": "Analysis", "order": 2}
                ]
            }
        }
    else:
        structure = {
            "structure": {
                "slides": [
                    {"id": "slide-1", "title": "Title Slide", "order": 0},
                    {"id": "slide-2", "title": "Overview", "order": 1},
                    {"id": "slide-3", "title": "Key Points", "order": 2}
                ]
            }
        }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/configure",
        json=structure,
        headers=headers
    )
    
    if response.status_code == 200:
        return project_id
    return None

def test_generation_status(token, project_id):
    """Test getting generation status"""
    print("\n=== Testing Generation Status ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}/generation-status",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_generate_all_content(token, project_id):
    """Test generating all content"""
    print("\n=== Testing Generate All Content ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Starting generation (this may take a while)...")
    start_time = time.time()
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/generate",
        headers=headers
    )
    
    elapsed_time = time.time() - start_time
    
    print(f"Status: {response.status_code}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    
    if response.status_code == 200:
        doc = response.json()
        content = doc.get("content", {})
        print(f"Generated content for {len(content)} items")
        # Show first item as sample
        if content:
            first_key = list(content.keys())[0]
            first_content = content[first_key]
            print(f"\nSample content ({first_key}):")
            print(first_content[:200] + "..." if len(first_content) > 200 else first_content)
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_generate_single_section(token, project_id):
    """Test generating single section"""
    print("\n=== Testing Generate Single Section ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"section_id": "section-2"}
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/generate-section",
        json=data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        content = response.json()
        print(f"Response: {json.dumps(content, indent=2)}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_generate_single_slide(token, project_id):
    """Test generating single slide"""
    print("\n=== Testing Generate Single Slide ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"slide_id": "slide-2"}
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/generate-slide",
        json=data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        content = response.json()
        print(f"Response: {json.dumps(content, indent=2)}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_get_document_with_content(token, project_id):
    """Test getting document with generated content"""
    print("\n=== Testing Get Document with Content ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}/document",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        doc = response.json()
        content = doc.get("content", {})
        print(f"Document has content for {len(content)} items")
        print(f"Document version: {doc.get('version')}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    print("Content Generation API Test Suite")
    print("=" * 50)
    print("\nNote: This requires GEMINI_API_KEY to be set in environment variables")
    print("=" * 50)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ Authentication failed. Cannot proceed with tests.")
        exit(1)
    
    # Test Word document generation
    print("\n" + "=" * 50)
    print("Testing Word Document Content Generation")
    print("=" * 50)
    
    word_project_id = create_and_configure_project(token, "word")
    if word_project_id:
        print(f"✅ Word project created and configured: {word_project_id}")
        
        if test_generation_status(token, word_project_id):
            print("✅ Generation status check successful")
        
        if test_generate_all_content(token, word_project_id):
            print("✅ Generate all content successful")
        
        if test_generation_status(token, word_project_id):
            print("✅ Generation status after generation successful")
        
        if test_generate_single_section(token, word_project_id):
            print("✅ Generate single section successful")
        
        if test_get_document_with_content(token, word_project_id):
            print("✅ Get document with content successful")
    
    # Test PowerPoint document generation
    print("\n" + "=" * 50)
    print("Testing PowerPoint Document Content Generation")
    print("=" * 50)
    
    ppt_project_id = create_and_configure_project(token, "powerpoint")
    if ppt_project_id:
        print(f"✅ PowerPoint project created and configured: {ppt_project_id}")
        
        if test_generation_status(token, ppt_project_id):
            print("✅ Generation status check successful")
        
        if test_generate_all_content(token, ppt_project_id):
            print("✅ Generate all content successful")
        
        if test_generate_single_slide(token, ppt_project_id):
            print("✅ Generate single slide successful")
        
        if test_get_document_with_content(token, ppt_project_id):
            print("✅ Get document with content successful")
    
    print("\n" + "=" * 50)
    print("Test suite completed")

