import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Helper function to extract error message from various error formats
const extractErrorMessage = (error) => {
  if (!error) return 'An error occurred';
  
  // If it's already a string, return it
  if (typeof error === 'string') return error;
  
  // If it's an array (validation errors), format them
  if (Array.isArray(error)) {
    return error.map(err => {
      if (typeof err === 'string') return err;
      if (err.msg) return `${err.loc?.join('.') || ''}: ${err.msg}`.trim();
      return JSON.stringify(err);
    }).join(', ');
  }
  
  // If it's an object, try to extract a message
  if (typeof error === 'object') {
    if (error.detail) {
      // FastAPI error detail can be string or array
      if (typeof error.detail === 'string') return error.detail;
      if (Array.isArray(error.detail)) {
        return error.detail.map(err => {
          if (typeof err === 'string') return err;
          if (err.msg) return `${err.loc?.join('.') || ''}: ${err.msg}`.trim();
          return JSON.stringify(err);
        }).join(', ');
      }
    }
    if (error.message) return error.message;
    if (error.msg) return error.msg;
  }
  
  // Fallback: stringify the error
  try {
    return JSON.stringify(error);
  } catch {
    return 'An error occurred';
  }
};

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    
    // Extract and attach a clean error message
    if (error.response?.data) {
      error.extractedMessage = extractErrorMessage(error.response.data);
    } else if (error.message) {
      error.extractedMessage = error.message;
    } else {
      error.extractedMessage = 'An error occurred';
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (email, password) =>
    api.post('/api/auth/register', { email, password }),
  
  login: (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
  
  getCurrentUser: () => api.get('/api/auth/me'),
};

// Projects API
export const projectsAPI = {
  getProjects: (skip = 0, limit = 100) =>
    api.get(`/api/projects?skip=${skip}&limit=${limit}`),
  
  getProject: (id) => api.get(`/api/projects/${id}`),
  
  createProject: (data) => api.post('/api/projects', data),
  
  updateProject: (id, data) => api.patch(`/api/projects/${id}`, data),
  
  deleteProject: (id) => api.delete(`/api/projects/${id}`),
};

// Documents API
export const documentsAPI = {
  configureDocument: (projectId, structure) =>
    api.post(`/api/projects/${projectId}/configure`, structure),
  
  getDocumentConfiguration: (projectId) =>
    api.get(`/api/projects/${projectId}/document`),
  
  updateDocumentStructure: (projectId, structure) =>
    api.put(`/api/projects/${projectId}/document/structure`, structure),
  
  reorderSections: (projectId, sectionOrders) =>
    api.post(`/api/projects/${projectId}/document/reorder-sections`, { section_orders: sectionOrders }),
  
  reorderSlides: (projectId, slideOrders) =>
    api.post(`/api/projects/${projectId}/document/reorder-slides`, { slide_orders: slideOrders }),
  
  aiSuggestTemplate: (projectId, documentType, mainTopic) =>
    api.post(`/api/projects/${projectId}/ai-suggest-template`, {
      document_type: documentType,
      main_topic: mainTopic,
    }),
};

// Generation API
export const generationAPI = {
  generateContent: (projectId) =>
    api.post(`/api/projects/${projectId}/generate`),
  
  getGenerationStatus: (projectId) =>
    api.get(`/api/projects/${projectId}/generation-status`),
};

// Refinement API
export const refinementAPI = {
  refineContent: (projectId, sectionId, prompt) =>
    api.post(`/api/projects/${projectId}/refine`, {
      section_id: sectionId,
      refinement_prompt: prompt,
    }),
  
  submitFeedback: (projectId, sectionId, feedback) =>
    api.post(`/api/projects/${projectId}/feedback`, {
      section_id: sectionId,
      feedback: feedback, // Can be "like", "dislike", or null to reset
    }),
  
  addComments: (projectId, sectionId, comments) =>
    api.post(`/api/projects/${projectId}/comments`, {
      section_id: sectionId,
      comments: comments,
    }),
  
  getRefinementHistory: (projectId, sectionId = null) => {
    const url = sectionId
      ? `/api/projects/${projectId}/refinement-history?section_id=${sectionId}`
      : `/api/projects/${projectId}/refinement-history`;
    return api.get(url);
  },
  
  getFeedback: (projectId) =>
    api.get(`/api/projects/${projectId}/feedback`),
};

// Export API
export const exportAPI = {
  exportDocument: (projectId) =>
    api.get(`/api/projects/${projectId}/export`, {
      responseType: 'blob',
    }),
  
  exportWord: (projectId) =>
    api.get(`/api/projects/${projectId}/export/docx`, {
      responseType: 'blob',
    }),
  
  exportPowerPoint: (projectId) =>
    api.get(`/api/projects/${projectId}/export/pptx`, {
      responseType: 'blob',
    }),
};

export default api;

