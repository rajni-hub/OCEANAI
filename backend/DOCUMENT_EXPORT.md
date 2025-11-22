# Document Export API Documentation

## Overview

The Document Export API allows users to export their finalized documents as `.docx` (Word) or `.pptx` (PowerPoint) files. The exported files include all sections/slides with the latest refined content, proper formatting, and structure preservation.

## Features

✅ **Word Export (.docx)** - Export Word documents with python-docx  
✅ **PowerPoint Export (.pptx)** - Export PowerPoint documents with python-pptx  
✅ **Latest Content** - Exports latest refined content from database  
✅ **Formatting Preservation** - Maintains structure and formatting  
✅ **Secure Download** - JWT-protected download endpoints  
✅ **Proper Structure** - Sections/slides in correct order  

## API Endpoints

### 1. Export Document (Auto-detect Type)
**GET** `/api/projects/{project_id}/export`

Export document as `.docx` or `.pptx` based on project document type.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (200 OK):**
- Returns downloadable file stream
- Content-Type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (Word)
- Content-Type: `application/vnd.openxmlformats-officedocument.presentationml.presentation` (PowerPoint)
- Content-Disposition: `attachment; filename="<project_title>_<timestamp>.<ext>"`

**Error Responses:**
- `400 Bad Request` - Invalid document type or structure
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or document not found
- `500 Internal Server Error` - Export generation error

**Example:**
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>/export" \
  -H "Authorization: Bearer <token>" \
  --output document.docx
```

---

### 2. Export Word Document
**GET** `/api/projects/{project_id}/export/docx`

Export document as `.docx` file (only for Word projects).

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (200 OK):**
- Returns downloadable `.docx` file stream
- Content-Type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- Content-Disposition: `attachment; filename="<project_title>_<timestamp>.docx"`

**Error Responses:**
- `400 Bad Request` - Project is not a Word document
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or document not found
- `500 Internal Server Error` - Export generation error

**Example:**
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>/export/docx" \
  -H "Authorization: Bearer <token>" \
  --output document.docx
```

---

### 3. Export PowerPoint Document
**GET** `/api/projects/{project_id}/export/pptx`

Export document as `.pptx` file (only for PowerPoint projects).

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `project_id` - Project UUID

**Response (200 OK):**
- Returns downloadable `.pptx` file stream
- Content-Type: `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- Content-Disposition: `attachment; filename="<project_title>_<timestamp>.pptx"`

**Error Responses:**
- `400 Bad Request` - Project is not a PowerPoint document
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Project or document not found
- `500 Internal Server Error` - Export generation error

**Example:**
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>/export/pptx" \
  -H "Authorization: Bearer <token>" \
  --output presentation.pptx
```

---

## Export Features

### Word Document Export

**Structure:**
- Document title (centered, heading level 1)
- Main topic subtitle (centered, italic)
- Sections as headings (level 2)
- Section content as paragraphs or bullet lists
- Proper spacing between sections

**Content Formatting:**
- Bullet points detected and formatted automatically
- Numbered lists detected and formatted
- Paragraphs with proper spacing
- Placeholder text for missing content (italic, gray)

**Document Properties:**
- Title: Project title
- Author: User email
- Comments: Generation timestamp

---

### PowerPoint Document Export

**Structure:**
- Title and Content layout for each slide
- Slide titles from structure
- Content in text frames
- Proper word wrapping

**Content Formatting:**
- Bullet points detected and formatted automatically
- Numbered lists detected and formatted
- Paragraphs with appropriate font sizes
- Placeholder text for missing content (italic, gray)

**Presentation Properties:**
- Title: Project title
- Author: User email
- Comments: Generation timestamp

---

## Export Process

### 1. Content Retrieval
- Fetches latest document structure from database
- Retrieves latest refined content for each section/slide
- Sorts sections/slides by order

### 2. Document Generation
- Creates Word or PowerPoint document
- Sets document properties (title, author, timestamp)
- Processes each section/slide in order

### 3. Content Formatting
- Detects bullet points and formats accordingly
- Detects numbered lists and formats accordingly
- Handles regular paragraphs with proper spacing
- Adds placeholder for missing content

### 4. File Generation
- Generates file in memory (BytesIO)
- Sets appropriate MIME type
- Generates filename with timestamp
- Returns as streaming response

---

## Usage Examples

### Export Word Document
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>/export" \
  -H "Authorization: Bearer <token>" \
  --output my_document.docx
```

### Export PowerPoint Document
```bash
curl -X GET "http://localhost:8000/api/projects/<project-id>/export" \
  -H "Authorization: Bearer <token>" \
  --output my_presentation.pptx
```

### Export with Specific Endpoint
```bash
# Word
curl -X GET "http://localhost:8000/api/projects/<project-id>/export/docx" \
  -H "Authorization: Bearer <token>" \
  --output document.docx

# PowerPoint
curl -X GET "http://localhost:8000/api/projects/<project-id>/export/pptx" \
  -H "Authorization: Bearer <token>" \
  --output presentation.pptx
```

---

## JavaScript/React Examples

### Export Document
```javascript
const exportDocument = async (projectId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/export`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    // Get filename from Content-Disposition header
    const contentDisposition = response.headers.get('Content-Disposition');
    const filename = contentDisposition
      ? contentDisposition.split('filename=')[1].replace(/"/g, '')
      : 'document.docx';
    
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } else {
    const error = await response.json();
    console.error('Export failed:', error);
  }
};

// Usage
await exportDocument(projectId);
```

### Export Word Document
```javascript
const exportWord = async (projectId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/export/docx`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'document.docx';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
};
```

### Export PowerPoint Document
```javascript
const exportPowerPoint = async (projectId) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/export/pptx`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'presentation.pptx';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
};
```

### Export with Progress (for large files)
```javascript
const exportDocumentWithProgress = async (projectId, onProgress) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(
    `http://localhost:8000/api/projects/${projectId}/export`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  if (!response.ok) {
    throw new Error('Export failed');
  }
  
  const reader = response.body.getReader();
  const contentLength = +response.headers.get('Content-Length');
  let receivedLength = 0;
  const chunks = [];
  
  while (true) {
    const { done, value } = await reader.read();
    
    if (done) break;
    
    chunks.push(value);
    receivedLength += value.length;
    
    if (onProgress && contentLength) {
      onProgress(receivedLength / contentLength);
    }
  }
  
  const blob = new Blob(chunks);
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'document.docx';
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};
```

---

## Export Quality Standards

### Word Documents
✅ **Structure**: Proper heading hierarchy  
✅ **Formatting**: Consistent paragraph spacing  
✅ **Lists**: Bullet and numbered lists properly formatted  
✅ **Content**: Latest refined content included  
✅ **Metadata**: Document properties set correctly  

### PowerPoint Documents
✅ **Structure**: Title and content layout  
✅ **Formatting**: Appropriate font sizes  
✅ **Lists**: Bullet points properly formatted  
✅ **Content**: Latest refined content included  
✅ **Metadata**: Presentation properties set correctly  

---

## Error Handling

All errors follow standard HTTP status codes:

- `400 Bad Request` - Invalid document type or structure
- `401 Unauthorized` - Missing or invalid authentication token
- `404 Not Found` - Project or document not found
- `500 Internal Server Error` - Export generation error

Error response format:
```json
{
  "detail": "Error message here"
}
```

---

## Security Considerations

1. **User Isolation**: Users can only export their own projects
2. **Token Validation**: All endpoints validate JWT tokens
3. **Content Validation**: Ensures document exists before export
4. **Project Ownership**: Every operation verifies project ownership
5. **Secure Download**: Files served with proper Content-Disposition headers

---

## Best Practices

1. **Generate Content First**: Ensure content is generated before exporting
2. **Refine Content**: Refine content before exporting for best results
3. **Check Structure**: Verify document structure is configured correctly
4. **Review Export**: Always review exported files for quality
5. **Handle Errors**: Implement proper error handling in frontend

---

## Testing

Use the provided test script:

```bash
# Start the server first
uvicorn app.main:app --reload

# In another terminal, run tests
python test_export.py
```

**Note:** Requires `GEMINI_API_KEY` to be set for content generation.

---

## File Naming

Exported files are named using the following format:
- `{project_title}_{timestamp}.{extension}`
- Example: `Market_Analysis_20240101_120000.docx`
- Special characters in project title are sanitized
- Timestamp format: `YYYYMMDD_HHMMSS`

---

**Status:** ✅ Phase 7 Complete - Document Export Implemented

