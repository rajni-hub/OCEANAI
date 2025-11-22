# Authentication System Documentation

## Overview

The authentication system uses **JWT (JSON Web Tokens)** for secure, stateless authentication. All passwords are hashed using **bcrypt** before storage.

## Security Features

✅ **JWT-based authentication** - No external dependencies  
✅ **Password hashing** - bcrypt with automatic salt  
✅ **Token expiration** - Configurable token lifetime (default: 30 minutes)  
✅ **Protected routes** - Middleware for route protection  
✅ **Password validation** - Minimum 8 characters  
✅ **Email validation** - Format validation  
✅ **Secure password storage** - Never stored in plain text  

## API Endpoints

### 1. Register User
**POST** `/api/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid email format or password too short
- `400 Bad Request` - Email already registered
- `500 Internal Server Error` - Server error

---

### 2. Login (Form Data)
**POST** `/api/auth/login`

Login using OAuth2 password flow (form data). This is the standard OAuth2 endpoint.

**Request (Form Data):**
```
username: user@example.com
password: securepassword123
```

**Response (200 OK):**
```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect email or password

---

### 3. Login (JSON)
**POST** `/api/auth/login-json`

Login using JSON body (alternative to form-based login).

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect email or password

---

### 4. Get Current User
**GET** `/api/auth/me`

Get information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token

---

### 5. Verify Token
**GET** `/api/auth/verify-token`

Verify if the current JWT token is valid.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (200 OK):**
```json
{
  "valid": true,
  "user_id": "uuid-here",
  "email": "user@example.com"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired token

---

### 6. Refresh Token
**POST** `/api/auth/refresh`

Get a new access token using the current valid token.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (200 OK):**
```json
{
  "access_token": "new-jwt-token-here",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired token

---

## Using Authentication in Protected Routes

### FastAPI Dependency

Use the `get_current_user` dependency to protect routes:

```python
from fastapi import Depends
from app.api.deps import get_current_user
from app.models.user import User

@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    # current_user is automatically validated
    return {"message": f"Hello {current_user.email}"}
```

### Client-Side Usage

Include the JWT token in the Authorization header:

```javascript
// JavaScript/React example
const token = localStorage.getItem('access_token');

fetch('http://localhost:8000/api/projects', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

```python
# Python example
import requests

token = "your-jwt-token-here"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
    "http://localhost:8000/api/projects",
    headers=headers
)
```

## Token Structure

JWT tokens contain:
- **sub**: User ID (UUID as string)
- **email**: User email
- **exp**: Expiration timestamp

Example payload:
```json
{
  "sub": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "exp": 1704067200
}
```

## Password Requirements

- Minimum 8 characters
- Stored as bcrypt hash (never plain text)
- Automatic salt generation

## Security Best Practices

1. **Never log passwords** - Passwords are never logged or exposed
2. **HTTPS in production** - Always use HTTPS for token transmission
3. **Token expiration** - Tokens expire after 30 minutes (configurable)
4. **Secure storage** - Store tokens securely on client (httpOnly cookies recommended)
5. **Token refresh** - Use refresh endpoint to get new tokens
6. **Validate on server** - Always validate tokens on the server side

## Environment Variables

Required authentication-related environment variables:

```env
SECRET_KEY=your-secret-key-here  # Used for JWT signing
ALGORITHM=HS256                   # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30    # Token expiration time
```

## Testing

Use the provided test script:

```bash
# Start the server first
uvicorn app.main:app --reload

# In another terminal, run tests
python test_auth.py
```

Or use curl:

```bash
# Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"

# Get current user (replace TOKEN with actual token)
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer TOKEN"
```

## Error Handling

All authentication errors follow standard HTTP status codes:

- `400 Bad Request` - Invalid input (email format, password length)
- `401 Unauthorized` - Authentication failed (wrong credentials, invalid token)
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```

## Implementation Details

### Password Hashing
- Uses `passlib` with `bcrypt` backend
- Automatic salt generation
- Secure password verification

### JWT Tokens
- Signed with HS256 algorithm
- Contains user ID and email
- Configurable expiration time
- Validated on every protected route access

### Database
- User passwords stored as hashes only
- Email addresses are unique and indexed
- User ID is UUID for security

---

**Status:** ✅ Phase 2 Complete - Authentication System Implemented

