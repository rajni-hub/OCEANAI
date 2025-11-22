"""
Simple test script for refinement endpoints
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

def create_and_generate_project(token, doc_type="word"):
    """Create, configure, and generate content for a test project"""
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
                    {"id": "section-2", "title": "Background", "order": 1}
                ]
            }
        }
    else:
        structure = {
            "structure": {
                "slides": [
                    {"id": "slide-1", "title": "Title Slide", "order": 0},
                    {"id": "slide-2", "title": "Overview", "order": 1}
                ]
            }
        }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/configure",
        json=structure,
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Failed to configure document: {response.text}")
        return None
    
    # Generate content
    print(f"Generating content for {doc_type} project...")
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/generate",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Failed to generate content: {response.text}")
        return None
    
    return project_id

def test_refine_content(token, project_id, section_id, doc_type="word"):
    """Test refining content with AI"""
    print(f"\n=== Testing Refine Content ({doc_type}) ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "section_id": section_id,
        "refinement_prompt": "Make this more formal and professional"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/refine",
        json=data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        refinement = response.json()
        print(f"Refinement ID: {refinement.get('id')}")
        print(f"Previous content length: {len(refinement.get('previous_content', ''))}")
        print(f"New content length: {len(refinement.get('new_content', ''))}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_submit_feedback(token, project_id, section_id):
    """Test submitting like/dislike feedback"""
    print("\n=== Testing Submit Feedback ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "section_id": section_id,
        "feedback": "like"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/feedback",
        json=data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        refinement = response.json()
        print(f"Feedback: {refinement.get('feedback')}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_add_comments(token, project_id, section_id):
    """Test adding comments"""
    print("\n=== Testing Add Comments ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "section_id": section_id,
        "comments": "This section needs more detail about market trends"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/comments",
        json=data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        refinement = response.json()
        print(f"Comments: {refinement.get('comments')}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_get_refinement_history(token, project_id, section_id=None):
    """Test getting refinement history"""
    print("\n=== Testing Get Refinement History ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    url = f"{BASE_URL}/api/projects/{project_id}/refinement-history"
    if section_id:
        url += f"?section_id={section_id}"
    
    response = requests.get(url, headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        history = response.json()
        print(f"Total refinements: {history.get('total')}")
        print(f"Returned refinements: {len(history.get('refinements', []))}")
        if history.get('refinements'):
            print(f"Latest refinement: {history['refinements'][0].get('id')}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_get_section_history(token, project_id, section_id):
    """Test getting refinement history for specific section"""
    print("\n=== Testing Get Section Refinement History ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}/refinement-history/{section_id}",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        history = response.json()
        print(f"Total refinements for section: {history.get('total')}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    print("Refinement Interface API Test Suite")
    print("=" * 50)
    print("\nNote: This requires GEMINI_API_KEY to be set for AI refinement")
    print("=" * 50)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ Authentication failed. Cannot proceed with tests.")
        exit(1)
    
    # Test Word document refinement
    print("\n" + "=" * 50)
    print("Testing Word Document Refinement")
    print("=" * 50)
    
    word_project_id = create_and_generate_project(token, "word")
    if word_project_id:
        print(f"✅ Word project created with content: {word_project_id}")
        
        section_id = "section-1"
        
        if test_refine_content(token, word_project_id, section_id, "word"):
            print("✅ Refine content successful")
        
        if test_submit_feedback(token, word_project_id, section_id):
            print("✅ Submit feedback successful")
        
        if test_add_comments(token, word_project_id, section_id):
            print("✅ Add comments successful")
        
        if test_get_refinement_history(token, word_project_id):
            print("✅ Get refinement history successful")
        
        if test_get_section_history(token, word_project_id, section_id):
            print("✅ Get section history successful")
        
        # Test another refinement
        if test_refine_content(token, word_project_id, section_id, "word"):
            print("✅ Second refinement successful")
    
    # Test PowerPoint document refinement
    print("\n" + "=" * 50)
    print("Testing PowerPoint Document Refinement")
    print("=" * 50)
    
    ppt_project_id = create_and_generate_project(token, "powerpoint")
    if ppt_project_id:
        print(f"✅ PowerPoint project created with content: {ppt_project_id}")
        
        slide_id = "slide-1"
        
        if test_refine_content(token, ppt_project_id, slide_id, "powerpoint"):
            print("✅ Refine slide content successful")
        
        if test_submit_feedback(token, ppt_project_id, slide_id):
            print("✅ Submit feedback successful")
        
        if test_add_comments(token, ppt_project_id, slide_id):
            print("✅ Add comments successful")
    
    print("\n" + "=" * 50)
    print("Test suite completed")

