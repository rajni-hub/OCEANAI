"""
Simple test script for export endpoints
Run this after starting the server and authenticating
"""
import requests
import json
import time
import os

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
        "title": f"Test {doc_type.title()} Export Project",
        "document_type": doc_type,
        "main_topic": "A comprehensive guide to renewable energy technologies"
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
                    {"id": "section-2", "title": "Solar Energy", "order": 1},
                    {"id": "section-3", "title": "Wind Energy", "order": 2}
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

def test_export_word(token, project_id):
    """Test exporting Word document"""
    print("\n=== Testing Word Document Export ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}/export",
        headers=headers,
        stream=True
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        # Save file
        filename = f"test_export_{int(time.time())}.docx"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Word document exported: {filename}")
        print(f"   File size: {os.path.getsize(filename)} bytes")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_export_powerpoint(token, project_id):
    """Test exporting PowerPoint document"""
    print("\n=== Testing PowerPoint Document Export ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}/export",
        headers=headers,
        stream=True
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        # Save file
        filename = f"test_export_{int(time.time())}.pptx"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ PowerPoint document exported: {filename}")
        print(f"   File size: {os.path.getsize(filename)} bytes")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_export_with_refinement(token, project_id, doc_type="word"):
    """Test exporting after refinement"""
    print("\n=== Testing Export After Refinement ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Refine a section/slide
    section_id = "section-1" if doc_type == "word" else "slide-1"
    refine_data = {
        "section_id": section_id,
        "refinement_prompt": "Make this more professional and add technical details"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/refine",
        json=refine_data,
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Content refined successfully")
    else:
        print(f"⚠️  Refinement failed: {response.text}")
    
    # Export document
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}/export",
        headers=headers,
        stream=True
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        extension = "docx" if doc_type == "word" else "pptx"
        filename = f"test_export_refined_{int(time.time())}.{extension}"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Refined document exported: {filename}")
        print(f"   File size: {os.path.getsize(filename)} bytes")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

if __name__ == "__main__":
    print("Document Export API Test Suite")
    print("=" * 50)
    print("\nNote: This requires GEMINI_API_KEY to be set for content generation")
    print("=" * 50)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ Authentication failed. Cannot proceed with tests.")
        exit(1)
    
    # Test Word document export
    print("\n" + "=" * 50)
    print("Testing Word Document Export")
    print("=" * 50)
    
    word_project_id = create_and_generate_project(token, "word")
    if word_project_id:
        print(f"✅ Word project created with content: {word_project_id}")
        
        if test_export_word(token, word_project_id):
            print("✅ Word export successful")
        
        if test_export_with_refinement(token, word_project_id, "word"):
            print("✅ Word export after refinement successful")
    
    # Test PowerPoint document export
    print("\n" + "=" * 50)
    print("Testing PowerPoint Document Export")
    print("=" * 50)
    
    ppt_project_id = create_and_generate_project(token, "powerpoint")
    if ppt_project_id:
        print(f"✅ PowerPoint project created with content: {ppt_project_id}")
        
        if test_export_powerpoint(token, ppt_project_id):
            print("✅ PowerPoint export successful")
        
        if test_export_with_refinement(token, ppt_project_id, "powerpoint"):
            print("✅ PowerPoint export after refinement successful")
    
    print("\n" + "=" * 50)
    print("Test suite completed")
    print("=" * 50)
    print("\nNote: Check the current directory for exported .docx and .pptx files")

