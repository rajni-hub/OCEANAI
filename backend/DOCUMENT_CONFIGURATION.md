# Document Configuration API Documentation

## Overview

The Document Configuration API allows users to configure document structures for their projects. It supports both Word documents (with sections/outline) and PowerPoint presentations (with slides). All endpoints require JWT authentication and ensure users can only configure documents for their own projects.

## Features

✅ **Word Document Configuration** - Create and manage document outlines with sections  
✅ **PowerPoint Configuration** - Define slides with titles  
✅ **Structure Validation** - Comprehensive validation for both document types  
✅ **Reorder Functionality** - Reorder sections or slides  
✅ **AI Template Generation** - Bonus feature for AI-suggested structures  
✅ **Version Tracking** - Document version increments on each update  

## API Endpoints

### 1. Configure Document
**POST** `/api/projects/{project_id}/configure`

Configure or update the document structure for a project.

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Path Parameters:**
- `project_id` - Project UUID

**Request Body (Word Document):**
```json
{
  "structure": {
    "sections": [
      {
        "id": "section-1",
        "title": "Introduction",
        "order": 0
      },
      {
        "id": "section-2",
        "title": "Background",
        "order": 1
      },
      {
        "id": "section-3",
        "title": "Analysis",
        "order": 2
      }
    ]
  }
}
```

**Request Body (PowerPoint Document):**
```json
{
  "structure": {
    "slides": [
      {
        "id": "slide-1",
        "title": "Title Slide",
        "order": 0
      },
      {
        "id": "slide-2",
        "title": "Overview",
        "order": 1
      },
      {
        "id": "slide-3",
        "title": "Key Points",
        "order": 2
      }
    ]
  }
}
```

**Response (200 OK):**
```json
{
  "id": "document-uuid",
  "project_id": "project-uuid",
  "structure": {
    "sections": [...]
  },
  "content": null,
  "version": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid structure format
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found or doesn't belong to user
- `500 Internal Server Error` - Server error

---

### 2. Get Document Configuration
**GET** `/api/projects/{project_id}/document`

Get the current document structure and content for a project.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (200 OK):**
```json
{
  "id": "document-uuid",
  "project_id": "project-uuid",
  "structure": {
    "sections": [...]
  },
  "content": null,
  "version": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found

---

### 3. Update Document Structure
**PUT** `/api/projects/{project_id}/document/structure`

Update the document structure (replaces existing structure).

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Path Parameters:**
- `project_id` - Project UUID

**Request Body:**
Same format as configure endpoint

**Response (200 OK):**
Updated document object

**Error Responses:**
- `400 Bad Request` - Invalid structure
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or document not found
- `500 Internal Server Error` - Server error

---

### 4. Reorder Sections (Word Only)
**POST** `/api/projects/{project_id}/document/reorder-sections`

Reorder sections in a Word document.

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Path Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "section-2": 0,
  "section-1": 1,
  "section-3": 2
}
```

Keys are section IDs, values are new order numbers.

**Response (200 OK):**
Updated document with reordered sections

**Error Responses:**
- `400 Bad Request` - Invalid orders or not a Word document
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or document not found

---

### 5. Reorder Slides (PowerPoint Only)
**POST** `/api/projects/{project_id}/document/reorder-slides`

Reorder slides in a PowerPoint document.

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Path Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "slide-2": 0,
  "slide-1": 1,
  "slide-3": 2
}
```

Keys are slide IDs, values are new order numbers.

**Response (200 OK):**
Updated document with reordered slides

**Error Responses:**
- `400 Bad Request` - Invalid orders or not a PowerPoint document
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or document not found

---

### 6. Generate AI Template (Bonus)
**POST** `/api/projects/{project_id}/generate-template`

Generate a document structure using AI based on the main topic.

**Headers:**
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Path Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "main_topic": "A market analysis of the EV industry in 2025",
  "document_type": "word"
}
```

**Response (200 OK):**
```json
{
  "structure": {
    "sections": [
      {
        "id": "section-1",
        "title": "Introduction",
        "order": 0
      },
      ...
    ]
  },
  "suggestions": [
    "You can customize the generated structure before applying it",
    "Add or remove sections/slides as needed",
    "Edit titles to match your requirements"
  ]
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request or document type mismatch
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found
- `500 Internal Server Error` - AI service error

**Note:** Requires `GEMINI_API_KEY` to be set in environment variables.

---

## Structure Validation

### Word Document Structure

**Required Fields:**
- `sections` (array) - List of sections

**Section Fields:**
- `id` (string) - Unique section identifier
- `title` (string) - Section title (1-255 characters)
- `order` (integer) - Section order (non-negative, unique)

**Validation Rules:**
- At least one section required
- Section IDs must be unique
- Section orders must be unique
- Titles cannot be empty

**Example:**
```json
{
  "sections": [
    {"id": "section-1", "title": "Introduction", "order": 0},
    {"id": "section-2", "title": "Background", "order": 1},
    {"id": "section-3", "title": "Analysis", "order": 2}
  ]
}
```

### PowerPoint Document Structure

**Required Fields:**
- `slides` (array) - List of slides

**Slide Fields:**
- `id` (string) - Unique slide identifier
- `title` (string) - Slide title (1-255 characters)
- `order` (integer) - Slide order (non-negative, unique)

**Validation Rules:**
- At least one slide required
- Slide IDs must be unique
- Slide orders must be unique
- Titles cannot be empty

**Example:**
```json
{
  "slides": [
    {"id": "slide-1", "title": "Title Slide", "order": 0},
    {"id": "slide-2", "title": "Overview", "order": 1},
    {"id": "slide-3", "title": "Key Points", "order": 2}
  ]
}
```

## Usage Examples

### Configure Word Document
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/configure" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "structure": {
      "sections": [
        {"id": "section-1", "title": "Introduction", "order": 0},
        {"id": "section-2", "title": "Background", "order": 1}
      ]
    }
  }'
```

### Configure PowerPoint Document
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/configure" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "structure": {
      "slides": [
        {"id": "slide-1", "title": "Title Slide", "order": 0},
        {"id": "slide-2", "title": "Overview", "order": 1}
      ]
    }
  }'
```

### Reorder Sections
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/document/reorder-sections" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "section-2": 0,
    "section-1": 1
  }'
```

### Generate AI Template
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/generate-template" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "main_topic": "A market analysis of the EV industry in 2025",
    "document_type": "word"
  }'
```

## JavaScript/React Examples

### Configure Document
```javascript
const configureDocument = async (projectId, structure) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/configure`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ structure })
    }
  );
  
  return await response.json();
};

// Word document
const wordStructure = {
  sections: [
    { id: "section-1", title: "Introduction", order: 0 },
    { id: "section-2", title: "Background", order: 1 }
  ]
};

// PowerPoint document
const pptStructure = {
  slides: [
    { id: "slide-1", title: "Title Slide", order: 0 },
    { id: "slide-2", title: "Overview", order: 1 }
  ]
};
```

### Get Document
```javascript
const getDocument = async (projectId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/document`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  return await response.json();
};
```

### Generate AI Template
```javascript
const generateTemplate = async (projectId, mainTopic, documentType) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/generate-template`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        main_topic: mainTopic,
        document_type: documentType
      })
    }
  );
  
  return await response.json();
};
```

## Error Handling

All errors follow standard HTTP status codes:

- `400 Bad Request` - Invalid structure format or validation error
- `401 Unauthorized` - Missing or invalid authentication token
- `404 Not Found` - Project or document not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```

## Security Considerations

1. **User Isolation**: Users can only configure documents for their own projects
2. **Token Validation**: All endpoints validate JWT tokens
3. **Input Validation**: All structures are validated before storage
4. **Project Ownership**: Every operation verifies project ownership
5. **Structure Validation**: Comprehensive validation prevents invalid data

## AI Template Generation (Bonus Feature)

The AI template generation feature uses Google's Gemini API to suggest document structures based on the main topic.

**Requirements:**
- `GEMINI_API_KEY` must be set in environment variables
- Project must exist and belong to the user
- Document type must match the project's document type

**How it works:**
1. User provides main topic and document type
2. System calls Gemini API with a structured prompt
3. AI generates a JSON structure with sections/slides
4. System validates and returns the structure
5. User can customize before applying

**Fallback:**
If AI generation fails, the system provides a basic default structure.

## Testing

Use the provided test script:

```bash
# Start the server first
uvicorn app.main:app --reload

# In another terminal, run tests
python test_documents.py
```

Or test manually using the API documentation at:
http://localhost:8000/api/docs

---

**Status:** ✅ Phase 4 Complete - Document Configuration Implemented

