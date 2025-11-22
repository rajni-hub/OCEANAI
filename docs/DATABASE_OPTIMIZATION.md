# Database Optimization - Refinements Table

## Overview

The refinements table has been optimized to reduce storage usage and improve performance by removing duplicate content storage.

## Changes Made

### 1. Refinement Model (`backend/app/models/refinement.py`)

**Removed Columns:**
- `previous_content` (Text) - Content before refinement
- `new_content` (Text) - Content after refinement

**Kept Columns:**
- `id` (UUID)
- `document_id` (UUID, FK)
- `section_id` (String)
- `refinement_prompt` (Text, nullable)
- `feedback` (Enum, nullable) - Deprecated, use Feedback table
- `comments` (Text, nullable)
- `created_at` (DateTime)

**New Indexes:**
- `idx_refinement_document_section` on (document_id, section_id)
- `idx_refinement_section_created` on (section_id, created_at)

### 2. Feedback Model (NEW)

Created a separate `Feedback` table for storing likes/dislikes:

**Columns:**
- `id` (UUID, PK)
- `document_id` (UUID, FK)
- `section_id` (String)
- `feedback_type` (Enum: LIKE/DISLIKE)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**Indexes:**
- `idx_feedback_document_section` on (document_id, section_id)
- `idx_feedback_section_created` on (section_id, created_at)
- `idx_feedback_unique_section` UNIQUE on (document_id, section_id) - One feedback per section

### 3. Document Model

**Single Source of Truth:**
- `documents.content` (JSON) now stores ALL section/slide content
- Content is never duplicated in refinements table
- Each refinement only stores metadata (prompt, comments, timestamps)

### 4. Refinement Service (`backend/app/services/refinement_service.py`)

**Changes:**
- `refine_section_with_ai()`: No longer stores content in Refinement record
- `refine_slide_with_ai()`: No longer stores content in Refinement record
- `submit_feedback()`: Now uses Feedback table instead of Refinement table
- `add_comment()`: No longer stores content in Refinement record
- `_limit_refinement_history()`: New function to limit history to last 3 per section
- `get_feedback_for_sections()`: New function to fetch feedback from Feedback table

### 5. API Routes (`backend/app/api/routes/refinement.py`)

**Updated Endpoints:**
- `POST /{project_id}/feedback`: Now returns `FeedbackResponse` instead of `RefinementResponse`
- `GET /{project_id}/feedback`: NEW endpoint to fetch all feedback for a project

**Response Changes:**
- `RefinementResponse` no longer includes `previous_content` or `new_content`
- New `FeedbackResponse` schema for feedback data

### 6. Schemas (`backend/app/schemas/refinement.py`)

**Updated:**
- `RefinementResponse`: Removed `previous_content` and `new_content` fields
- `FeedbackResponse`: NEW schema for feedback data

## Migration

### Migration Script

Location: `backend/migrations/optimize_refinements_table.py`

**Steps:**
1. Creates `feedback` table
2. Migrates existing feedback data from `refinements` to `feedback`
3. Adds indexes for performance
4. Removes `previous_content` and `new_content` columns from `refinements`
5. Limits refinement history to last 3 per section

**To Run:**
```bash
cd backend
python migrations/optimize_refinements_table.py
```

**Note:** SQLite doesn't support `DROP COLUMN`, so the migration recreates the table.

## Benefits

### Storage Reduction
- **Before:** Each refinement stored full content (previous + new) = ~2x content size
- **After:** Only metadata stored = ~1% of previous size
- **Example:** 100 refinements of 1000-char sections = 200KB → 2KB (99% reduction)

### Performance Improvements
- Faster queries (smaller table size)
- Better index usage (composite indexes)
- Reduced I/O operations

### Scalability
- Refinement history limited to last 3 per section (prevents unlimited growth)
- Separate Feedback table for better query performance
- Content stored once in `documents.content`

## Backward Compatibility

The frontend has been updated to:
1. Use new `GET /api/projects/{id}/feedback` endpoint
2. Fallback to refinement history if new endpoint fails (for compatibility)

## Testing

After migration, verify:
1. ✅ Refinements table has no content columns
2. ✅ Feedback table exists and has data
3. ✅ Content is stored only in `documents.content`
4. ✅ Refinement history is limited to last 3 per section
5. ✅ All indexes are created
6. ✅ API endpoints work correctly
7. ✅ Frontend can fetch and display feedback

## Rollback

If needed, you can rollback by:
1. Restoring from database backup
2. Reverting code changes
3. Re-running old migration

**Note:** Always backup your database before running migrations!

