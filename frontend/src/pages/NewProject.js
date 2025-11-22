import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { projectsAPI } from '../services/api';
import './NewProject.css';

const NewProject = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [title, setTitle] = useState('');
  const [documentType, setDocumentType] = useState('word');
  const [mainTopic, setMainTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isExiting, setIsExiting] = useState(false);

  // Handle document type from navigation state
  useEffect(() => {
    if (location.state?.documentType) {
      setDocumentType(location.state.documentType);
    }
    // Reset exit state when component mounts
    setIsExiting(false);
  }, [location.state]);

  // Handle navigation back to dashboard with transition
  useEffect(() => {
    const handleNavigation = (e) => {
      // Check if clicking on Dashboard link in navbar
      const navLink = e.target.closest('a[href="/dashboard"], a[href="/"]');
      if (navLink && location.pathname === '/projects/new') {
        e.preventDefault();
        e.stopPropagation();
        setIsExiting(true);
        setTimeout(() => {
          const href = navLink.getAttribute('href');
          navigate(href === '/' ? '/dashboard' : href);
        }, 300);
      }
    };

    // Use capture phase to catch the event early
    document.addEventListener('click', handleNavigation, true);
    return () => document.removeEventListener('click', handleNavigation, true);
  }, [navigate, location.pathname]);

  // Handle cancel/back navigation with transition
  const handleCancel = () => {
    setIsExiting(true);
    setTimeout(() => {
      navigate('/dashboard');
    }, 300);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await projectsAPI.createProject({
        title,
        document_type: documentType,
        main_topic: mainTopic,
      });
      
      navigate(`/projects/${response.data.id}`);
    } catch (err) {
      const errorMsg = err.extractedMessage || err.response?.data?.detail || err.message || 'Failed to create project';
      setError(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`new-project-container ${isExiting ? 'exiting' : ''}`}>
      <div className="container">
        <div className="page-header">
          <h1>Create New Project</h1>
          <p>Start building your AI-powered document</p>
        </div>
        
        <div className="new-project-card card">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Project Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                placeholder="e.g., Q4 Business Report"
              />
            </div>
            
            <div className="form-group">
              <label>Document Type</label>
              <div className="document-type-selector">
                <div
                  className={`type-option ${documentType === 'word' ? 'selected' : ''}`}
                  onClick={() => setDocumentType('word')}
                >
                  <div className="type-option-label">Word Document</div>
                  <div className="type-option-desc">Structured documents</div>
                </div>
                <div
                  className={`type-option ${documentType === 'powerpoint' ? 'selected' : ''}`}
                  onClick={() => setDocumentType('powerpoint')}
                >
                  <div className="type-option-label">PowerPoint</div>
                  <div className="type-option-desc">Presentations</div>
                </div>
              </div>
            </div>
            
            <div className="form-group">
              <label>Main Topic</label>
              <textarea
                value={mainTopic}
                onChange={(e) => setMainTopic(e.target.value)}
                required
                placeholder="Describe the main topic, theme, or purpose of your document..."
                rows="5"
              />
            </div>
            
            {error && <div className="error">{error}</div>}
            
            <div className="form-actions">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={handleCancel}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <div className="spinner spinner-small"></div>
                    <span>Creating</span>
                  </>
                ) : (
                  'Create project'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default NewProject;
