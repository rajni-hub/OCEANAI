# Project Management API Documentation

## Overview

The Project Management API provides full CRUD (Create, Read, Update, Delete) operations for document projects. All endpoints require JWT authentication and ensure that users can only access their own projects.

## Security Features

✅ **JWT Authentication Required** - All endpoints are protected  
✅ **User Isolation** - Users can only access their own projects  
✅ **Input Validation** - Pydantic schema validation  
✅ **Error Handling** - Proper HTTP status codes  
✅ **Cascade Deletion** - Projects are deleted when user is deleted  

## API Endpoints

### 1. Create Project
**POST** `/api/projects`

Create a new document project for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Market Analysis Report",
  "document_type": "word",
  "main_topic": "A market analysis of the EV industry in 2025"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-here",
  "user_id": "user-uuid-here",
  "title": "Market Analysis Report",
  "document_type": "word",
  "main_topic": "A market analysis of the EV industry in 2025",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input (empty title/topic, invalid document_type)
- `401 Unauthorized` - Missing or invalid token
- `500 Internal Server Error` - Server error

---

### 2. List Projects
**GET** `/api/projects`

Get all projects belonging to the authenticated user with pagination.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Query Parameters:**
- `skip` (optional, default: 0) - Number of records to skip
- `limit` (optional, default: 100, max: 1000) - Maximum number of records to return

**Example:**
```
GET /api/projects?skip=0&limit=10
```

**Response (200 OK):**
```json
{
  "projects": [
    {
      "id": "uuid-here",
      "user_id": "user-uuid-here",
      "title": "Market Analysis Report",
      "document_type": "word",
      "main_topic": "A market analysis of the EV industry in 2025",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `500 Internal Server Error` - Server error

---

### 3. Get Project by ID
**GET** `/api/projects/{project_id}`

Get a specific project by ID. Only returns the project if it belongs to the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "user_id": "user-uuid-here",
  "title": "Market Analysis Report",
  "document_type": "word",
  "main_topic": "A market analysis of the EV industry in 2025",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found or doesn't belong to user
- `500 Internal Server Error` - Server error

---

### 4. Update Project
**PUT** `/api/projects/{project_id}`

Update a project. Only updates if the project belongs to the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Path Parameters:**
- `project_id` - Project UUID

**Request Body (all fields optional):**
```json
{
  "title": "Updated Title",
  "main_topic": "Updated topic"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "user_id": "user-uuid-here",
  "title": "Updated Title",
  "document_type": "word",
  "main_topic": "Updated topic",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:01:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found or doesn't belong to user
- `500 Internal Server Error` - Server error

---

### 5. Delete Project
**DELETE** `/api/projects/{project_id}`

Delete a project. Only deletes if the project belongs to the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (204 No Content):**
No response body

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found or doesn't belong to user
- `500 Internal Server Error` - Server error

---

### 6. Check Project Exists
**GET** `/api/projects/{project_id}/exists`

Check if a project exists and belongs to the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (200 OK):**
```json
{
  "exists": true,
  "project_id": "uuid-here"
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token

---

## Data Models

### Project
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to User
- `title` (String, 1-255 chars) - Project title
- `document_type` (Enum) - "word" or "powerpoint"
- `main_topic` (String, 1-500 chars) - Main topic or prompt
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### Document Types
- `word` - Microsoft Word document (.docx)
- `powerpoint` - Microsoft PowerPoint document (.pptx)

## Validation Rules

### Title
- Required
- Minimum length: 1 character
- Maximum length: 255 characters
- Cannot be empty or whitespace only

### Main Topic
- Required
- Minimum length: 1 character
- Maximum length: 500 characters
- Cannot be empty or whitespace only

### Document Type
- Required
- Must be either "word" or "powerpoint"
- Enum validation

## Usage Examples

### Create a Word Project
```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Market Analysis",
    "document_type": "word",
    "main_topic": "A market analysis of the EV industry in 2025"
  }'
```

### Create a PowerPoint Project
```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Product Presentation",
    "document_type": "powerpoint",
    "main_topic": "Introduction to our new product line"
  }'
```

### List All Projects
```bash
curl -X GET "http://localhost:8000/api/projects?skip=0&limit=10" \
  -H "Authorization: Bearer <token>"
```

### Get Specific Project
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>" \
  -H "Authorization: Bearer <token>"
```

### Update Project
```bash
curl -X PUT "http://localhost:8000/api/projects/<project-id>" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "main_topic": "Updated topic"
  }'
```

### Delete Project
```bash
curl -X DELETE "http://localhost:8000/api/projects/<project-id>" \
  -H "Authorization: Bearer <token>"
```

## JavaScript/React Examples

### Create Project
```javascript
const createProject = async (projectData) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/api/projects', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(projectData)
  });
  
  return await response.json();
};

// Usage
const project = await createProject({
  title: "Market Analysis",
  document_type: "word",
  main_topic: "A market analysis of the EV industry in 2025"
});
```

### List Projects
```javascript
const listProjects = async (skip = 0, limit = 100) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects?skip=${skip}&limit=${limit}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  return await response.json();
};
```

### Update Project
```javascript
const updateProject = async (projectId, updates) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updates)
    }
  );
  
  return await response.json();
};
```

### Delete Project
```javascript
const deleteProject = async (projectId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}`,
    {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  return response.status === 204;
};
```

## Error Handling

All errors follow standard HTTP status codes:

- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid authentication token
- `404 Not Found` - Project not found or doesn't belong to user
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```

## Security Considerations

1. **User Isolation**: Users can only access their own projects
2. **Token Validation**: All endpoints validate JWT tokens
3. **Input Validation**: All inputs are validated using Pydantic schemas
4. **Cascade Deletion**: Projects are automatically deleted when user is deleted
5. **No Direct ID Access**: Project IDs are validated against user ownership

## Testing

Use the provided test script:

```bash
# Start the server first
uvicorn app.main:app --reload

# In another terminal, run tests
python test_projects.py
```

Or test manually using the API documentation at:
http://localhost:8000/api/docs

---

**Status:** ✅ Phase 3 Complete - Project Management Implemented

