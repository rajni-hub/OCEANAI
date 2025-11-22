# Content Generation API Documentation

## Overview

The Content Generation API uses Google's Gemini AI to generate content for document sections (Word) and slides (PowerPoint). Content is generated section-by-section or slide-by-slide, with context awareness and proper error handling.

## Features

✅ **Section-by-Section Generation** - Generate content for Word document sections  
✅ **Slide-by-Slide Generation** - Generate content for PowerPoint slides  
✅ **Context-Aware Generation** - Uses previous sections/slides for context  
✅ **Retry Logic** - Automatic retries on AI failures (3 attempts)  
✅ **Error Handling** - Graceful error handling with fallbacks  
✅ **Progress Tracking** - Check generation status and progress  
✅ **Single Item Generation** - Generate content for individual sections/slides  

## Prerequisites

- `GEMINI_API_KEY` must be set in environment variables
- Document structure must be configured before generation
- Project must exist and belong to authenticated user

## API Endpoints

### 1. Generate All Content
**POST** `/api/projects/{project_id}/generate`

Generate content for all sections (Word) or slides (PowerPoint) in the document.

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
  "content": {
    "section-1": "Generated content for section 1...",
    "section-2": "Generated content for section 2...",
    "section-3": "Generated content for section 3..."
  },
  "version": 2,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:01:00"
}
```

**Error Responses:**
- `400 Bad Request` - Document structure not configured
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or document not found
- `500 Internal Server Error` - AI generation error

**Note:** This endpoint may take some time depending on the number of sections/slides.

---

### 2. Generate Single Section (Word Only)
**POST** `/api/projects/{project_id}/generate-section`

Generate content for a single section in a Word document.

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
  "section_id": "section-2"
}
```

**Response (200 OK):**
```json
{
  "section-2": "Generated content for this section..."
}
```

**Error Responses:**
- `400 Bad Request` - Not a Word document or section not found
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or section not found
- `500 Internal Server Error` - AI generation error

---

### 3. Generate Single Slide (PowerPoint Only)
**POST** `/api/projects/{project_id}/generate-slide`

Generate content for a single slide in a PowerPoint document.

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
  "slide_id": "slide-2"
}
```

**Response (200 OK):**
```json
{
  "slide-2": "Generated content for this slide..."
}
```

**Error Responses:**
- `400 Bad Request` - Not a PowerPoint document or slide not found
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or slide not found
- `500 Internal Server Error` - AI generation error

---

### 4. Get Generation Status
**GET** `/api/projects/{project_id}/generation-status`

Get the status of content generation for a document.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (200 OK) - Word Document:**
```json
{
  "status": "completed",
  "total_sections": 3,
  "generated_sections": 3,
  "progress_percentage": 100
}
```

**Response (200 OK) - PowerPoint Document:**
```json
{
  "status": "partial",
  "total_slides": 5,
  "generated_slides": 3,
  "progress_percentage": 60
}
```

**Response (200 OK) - Not Configured:**
```json
{
  "status": "not_configured",
  "message": "Document structure not configured yet"
}
```

**Status Values:**
- `not_configured` - Document structure not set up
- `partial` - Some content generated, but not all
- `completed` - All content generated

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project not found

---

## Content Generation Details

### Word Document Content

**Generation Process:**
1. Iterates through sections in order
2. For each section:
   - Builds context from previous sections
   - Generates 3-5 paragraphs (300-500 words)
   - Stores content with section ID as key

**Content Format:**
- Professional, well-structured paragraphs
- Contextually relevant to main topic
- Includes relevant information and analysis

**Storage:**
```json
{
  "section-1": "Content text for section 1...",
  "section-2": "Content text for section 2...",
  ...
}
```

### PowerPoint Document Content

**Generation Process:**
1. Iterates through slides in order
2. For each slide:
   - Builds context from previous slides
   - Generates bullet-point style content
   - Stores content with slide ID as key

**Content Format:**
- Concise, bullet-point style
   - 3-6 key points per slide
   - Brief and impactful
   - Suitable for presentation

**Storage:**
```json
{
  "slide-1": "• Point 1\n• Point 2\n• Point 3",
  "slide-2": "• Point 1\n• Point 2\n...",
  ...
}
```

## Error Handling & Retries

### Retry Logic
- **Maximum Retries**: 3 attempts
- **Delay**: Exponential backoff (1s, 2s, 3s)
- **Retry Conditions**: API errors, network failures, timeouts

### Error Responses
If all retries fail, the system:
- Returns an error message
- Does not store partial content
- Allows user to retry manually

### Fallback Behavior
If AI generation fails completely:
- Returns placeholder text indicating failure
- Allows manual content entry
- User can retry generation later

## Usage Examples

### Generate All Content
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/generate" \
  -H "Authorization: Bearer <token>"
```

### Generate Single Section
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/generate-section" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"section_id": "section-2"}'
```

### Generate Single Slide
```bash
curl -X POST "http://localhost:8000/api/projects/<project-id>/generate-slide" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"slide_id": "slide-2"}'
```

### Check Generation Status
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>/generation-status" \
  -H "Authorization: Bearer <token>"
```

## JavaScript/React Examples

### Generate All Content
```javascript
const generateAllContent = async (projectId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/generate`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  if (response.ok) {
    const document = await response.json();
    console.log('Generated content:', document.content);
    return document;
  } else {
    throw new Error('Generation failed');
  }
};
```

### Generate Single Section
```javascript
const generateSection = async (projectId, sectionId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/generate-section`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ section_id: sectionId })
    }
  );
  
  return await response.json();
};
```

### Check Generation Status
```javascript
const checkGenerationStatus = async (projectId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/generation-status`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  return await response.json();
};
```

### Polling for Generation Progress
```javascript
const pollGenerationStatus = async (projectId, onProgress) => {
  const interval = setInterval(async () => {
    const status = await checkGenerationStatus(projectId);
    onProgress(status);
    
    if (status.status === 'completed') {
      clearInterval(interval);
    }
  }, 2000); // Check every 2 seconds
  
  return interval;
};
```

## Context-Aware Generation

The AI generation is context-aware:

1. **Previous Sections/Slides**: Content from previous items is included in the prompt
2. **Main Topic**: The project's main topic is always included
3. **Section/Slide Title**: The specific title is used for focused generation
4. **Order Awareness**: Content is generated in order to maintain flow

**Example Context:**
```
Main Topic: A market analysis of the EV industry in 2025
Previous Sections:
- Introduction
- Background
Current Section: Analysis
```

## Rate Limiting Considerations

- **Delay Between Requests**: 0.5 seconds between section/slide generation
- **API Limits**: Respects Gemini API rate limits
- **Batch Generation**: All content generated in sequence
- **Single Item Generation**: Faster for individual items

## Best Practices

1. **Configure Structure First**: Always configure document structure before generation
2. **Check Status**: Use status endpoint to monitor progress
3. **Handle Errors**: Implement retry logic on client side if needed
4. **Progress Indicators**: Show progress to users during generation
5. **Single Item Generation**: Use for regenerating specific sections/slides
6. **Content Review**: Always review generated content before export

## Testing

Use the provided test script:

```bash
# Start the server first
uvicorn app.main:app --reload

# In another terminal, run tests
python test_generation.py
```

**Note:** Requires `GEMINI_API_KEY` to be set in environment variables.

## Troubleshooting

### Generation Fails
- Check `GEMINI_API_KEY` is set correctly
- Verify API key has sufficient quota
- Check network connectivity
- Review error messages in response

### Partial Generation
- Use status endpoint to check progress
- Generate missing sections/slides individually
- Retry failed items

### Slow Generation
- Normal for documents with many sections/slides
- Consider generating sections individually
- Use status endpoint to show progress

---

**Status:** ✅ Phase 5 Complete - Content Generation Implemented

