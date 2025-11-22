# Refinement Interface API Documentation

## Overview

The Refinement Interface API allows users to refine generated content using AI, provide feedback (like/dislike), and add comments. All refinements are tracked in history with version control, and the document content is updated accordingly.

## Features

✅ **AI-Powered Refinement** - Refine content using natural language prompts  
✅ **Like/Dislike Feedback** - Quick feedback mechanism  
✅ **Comments System** - Add detailed comments per section/slide  
✅ **Refinement History** - Complete history tracking with version control  
✅ **Content Updates** - Refinements automatically update document content  
✅ **Section/Slide-Wise** - Refine individual sections or slides  

## API Endpoints

### 1. Refine Content with AI
**POST** `/api/projects/{project_id}/refine`

Refine content for a section (Word) or slide (PowerPoint) using AI based on a user's refinement prompt.

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
  "section_id": "section-1",
  "refinement_prompt": "Make this more formal and professional"
}
```

**Example Prompts:**
- "Make this more formal"
- "Convert to bullet points"
- "Shorten to 100 words"
- "Add more technical details"
- "Make it more concise"
- "Use simpler language"

**Response (200 OK):**
```json
{
  "id": "refinement-uuid",
  "document_id": "document-uuid",
  "section_id": "section-1",
  "refinement_prompt": "Make this more formal and professional",
  "previous_content": "Original content text...",
  "new_content": "Refined content text...",
  "feedback": null,
  "comments": null,
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request or content not found
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project, document, or section/slide not found
- `500 Internal Server Error` - AI generation error

**Note:** This endpoint updates the document content automatically.

---

### 2. Submit Like/Dislike Feedback
**POST** `/api/projects/{project_id}/feedback`

Submit like or dislike feedback for a section or slide.

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
  "section_id": "section-1",
  "feedback": "like"
}
```

**Feedback Values:**
- `"like"` - Positive feedback
- `"dislike"` - Negative feedback

**Response (201 Created):**
```json
{
  "id": "refinement-uuid",
  "document_id": "document-uuid",
  "section_id": "section-1",
  "refinement_prompt": null,
  "previous_content": null,
  "new_content": "Current content...",
  "feedback": "like",
  "comments": null,
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid feedback or content not found
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or section/slide not found

---

### 3. Add Comments
**POST** `/api/projects/{project_id}/comments`

Add comments for a section or slide.

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
  "section_id": "section-1",
  "comments": "This section needs more detail about market trends and should include recent statistics"
}
```

**Response (201 Created):**
```json
{
  "id": "refinement-uuid",
  "document_id": "document-uuid",
  "section_id": "section-1",
  "refinement_prompt": null,
  "previous_content": null,
  "new_content": "Current content...",
  "feedback": null,
  "comments": "This section needs more detail about market trends and should include recent statistics",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid comments or content not found
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or section/slide not found

---

### 4. Get Refinement History
**GET** `/api/projects/{project_id}/refinement-history`

Get refinement history for a document, optionally filtered by section/slide.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Query Parameters:**
- `section_id` (optional) - Filter by section/slide ID
- `skip` (optional, default: 0) - Pagination offset
- `limit` (optional, default: 100, max: 1000) - Pagination limit

**Example:**
```
GET /api/projects/{id}/refinement-history?section_id=section-1&skip=0&limit=50
```

**Response (200 OK):**
```json
{
  "refinements": [
    {
      "id": "refinement-uuid-1",
      "document_id": "document-uuid",
      "section_id": "section-1",
      "refinement_prompt": "Make this more formal",
      "previous_content": "Original content...",
      "new_content": "Refined content...",
      "feedback": "like",
      "comments": "Good improvement",
      "created_at": "2024-01-01T00:01:00"
    },
    {
      "id": "refinement-uuid-2",
      "document_id": "document-uuid",
      "section_id": "section-1",
      "refinement_prompt": null,
      "previous_content": null,
      "new_content": "Current content...",
      "feedback": null,
      "comments": "Needs more detail",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 2,
  "section_id": "section-1"
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found

---

### 5. Get Section/Slide Refinement History
**GET** `/api/projects/{project_id}/refinement-history/{section_id}`

Get refinement history for a specific section or slide.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID
- `section_id` - Section or slide ID

**Query Parameters:**
- `skip` (optional, default: 0) - Pagination offset
- `limit` (optional, default: 100, max: 1000) - Pagination limit

**Response (200 OK):**
Same format as general refinement history, but filtered to the specific section/slide.

---

## Refinement Process

### AI Refinement Flow

1. **User provides refinement prompt** (e.g., "Make this more formal")
2. **System retrieves current content** for the section/slide
3. **AI generates refined content** based on prompt and context
4. **Refinement record created** with previous and new content
5. **Document content updated** automatically
6. **Document version incremented**

### Feedback Flow

1. **User clicks like/dislike** for a section/slide
2. **Refinement record created** with feedback
3. **Content remains unchanged** (feedback only)
4. **History tracked** for analytics

### Comments Flow

1. **User adds comments** for a section/slide
2. **Refinement record created** with comments
3. **Content remains unchanged** (comments only)
4. **History tracked** for reference

## Refinement History

### What's Tracked

- **AI Refinements**: Previous content, new content, refinement prompt
- **Feedback**: Like/dislike votes
- **Comments**: User notes and observations
- **Timestamps**: When each refinement occurred
- **Section/Slide ID**: Which item was refined

### Version Tracking

- Document version increments on each AI refinement
- Refinement history provides complete audit trail
- Can see evolution of content over time

## Usage Examples

### Refine Content
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/refine" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "section_id": "section-1",
    "refinement_prompt": "Make this more formal and professional"
  }'
```

### Submit Feedback
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/feedback" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "section_id": "section-1",
    "feedback": "like"
  }'
```

### Add Comments
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/comments" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "section_id": "section-1",
    "comments": "This section needs more technical details"
  }'
```

### Get Refinement History
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>/refinement-history?section_id=section-1" \
  -H "Authorization: Bearer <token>"
```

## JavaScript/React Examples

### Refine Content
```javascript
const refineContent = async (projectId, sectionId, prompt) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/refine`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        section_id: sectionId,
        refinement_prompt: prompt
      })
    }
  );
  
  return await response.json();
};

// Usage
const refinement = await refineContent(
  projectId,
  "section-1",
  "Make this more concise"
);
```

### Submit Feedback
```javascript
const submitFeedback = async (projectId, sectionId, feedback) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/feedback`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        section_id: sectionId,
        feedback: feedback // "like" or "dislike"
      })
    }
  );
  
  return await response.json();
};
```

### Add Comments
```javascript
const addComments = async (projectId, sectionId, comments) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/comments`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        section_id: sectionId,
        comments: comments
      })
    }
  );
  
  return await response.json();
};
```

### Get Refinement History
```javascript
const getRefinementHistory = async (projectId, sectionId = null) => {
  const token = localStorage.getItem('access_token');
  
  let url = `http://localhost:8000/api/projects/${projectId}/refinement-history`;
  if (sectionId) {
    url += `?section_id=${sectionId}`;
  }
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
};
```

## Refinement Prompt Examples

### Style Refinements
- "Make this more formal"
- "Make this more casual"
- "Use professional business language"
- "Write in a conversational tone"

### Format Refinements
- "Convert to bullet points"
- "Convert to paragraphs"
- "Make this a numbered list"
- "Format as a table"

### Length Refinements
- "Shorten to 100 words"
- "Expand to 500 words"
- "Make this more concise"
- "Add more detail"

### Content Refinements
- "Add more technical details"
- "Include recent statistics"
- "Add examples"
- "Focus on benefits"
- "Emphasize risks"

## Error Handling

All errors follow standard HTTP status codes:

- `400 Bad Request` - Invalid request or content not found
- `401 Unauthorized` - Missing or invalid authentication token
- `404 Not Found` - Project, document, or section/slide not found
- `500 Internal Server Error` - AI generation error

Error response format:
```json
{
  "detail": "Error message here"
}
```

## Security Considerations

1. **User Isolation**: Users can only refine their own projects
2. **Token Validation**: All endpoints validate JWT tokens
3. **Content Validation**: Ensures content exists before refinement
4. **Project Ownership**: Every operation verifies project ownership
5. **History Tracking**: Complete audit trail of all changes

## Best Practices

1. **Generate Content First**: Ensure content is generated before refining
2. **Clear Prompts**: Use specific, clear refinement prompts
3. **Review Changes**: Always review refined content before accepting
4. **Use Feedback**: Provide feedback to improve future generations
5. **Track History**: Review refinement history to understand changes
6. **Iterative Refinement**: Refine multiple times if needed

## Testing

Use the provided test script:

```bash
# Start the server first
uvicorn app.main:app --reload

# In another terminal, run tests
python test_refinement.py
```

**Note:** Requires `GEMINI_API_KEY` to be set for AI refinement features.

---

**Status:** ✅ Phase 6 Complete - Refinement Interface Implemented

