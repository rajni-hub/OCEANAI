import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectsAPI, documentsAPI, generationAPI, refinementAPI, exportAPI } from '../services/api';
import DocumentConfiguration from '../components/DocumentConfiguration';
import ContentGeneration from '../components/ContentGeneration';
import RefinementInterface from '../components/RefinementInterface';
import './ProjectDetail.css';

const ProjectDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [document, setDocument] = useState(null);
  const [activeTab, setActiveTab] = useState('configure');
  const [loading, setLoading] = useState(true);
  const [exportLoading, setExportLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Preserve active tab across updates
  const activeTabRef = useRef('configure');
  
  useEffect(() => {
    activeTabRef.current = activeTab;
  }, [activeTab]);

  useEffect(() => {
    loadProject();
  }, [id]);

  const loadProject = async () => {
    // CRITICAL: Don't set loading to true if we're just refreshing
    // This prevents the component from unmounting
    // Declare outside try block so it's accessible in finally
    const isRefreshing = project !== null && document !== null;
    
    try {
      // Preserve active tab before loading
      const preservedTab = activeTabRef.current;
      
      console.log('[LOAD_PROJECT] ============================================');
      console.log('[LOAD_PROJECT] Starting loadProject...');
      console.log('[LOAD_PROJECT]   Current activeTab:', activeTab);
      console.log('[LOAD_PROJECT]   Preserved tab:', preservedTab);
      console.log('[LOAD_PROJECT]   Project ID:', id);
      console.log('[LOAD_PROJECT]   Current project exists:', project !== null);
      console.log('[LOAD_PROJECT]   Current document exists:', document !== null);
      console.log('[LOAD_PROJECT]   Is refreshing (not initial load):', isRefreshing);
      console.log('[LOAD_PROJECT] ============================================');
      
      const projectRes = await projectsAPI.getProject(id);
      let docRes = null;
      try {
        docRes = await documentsAPI.getDocumentConfiguration(id);
        console.log('[LOAD_PROJECT] Document loaded:', {
          id: docRes?.data?.id,
          version: docRes?.data?.version,
          contentKeys: Object.keys(docRes?.data?.content || {}),
          contentPreview: docRes?.data?.content ? Object.fromEntries(
            Object.entries(docRes.data.content).map(([k, v]) => [k, typeof v === 'string' ? v.substring(0, 50) + '...' : v])
          ) : null
        });
      } catch (err) {
        // Document might not exist yet
        console.log('[LOAD_PROJECT] Document not found or error:', err);
        docRes = null;
      }
      
      console.log('[LOAD_PROJECT] Updating state...');
      console.log('[LOAD_PROJECT]   Will setProject:', projectRes.data?.id);
      console.log('[LOAD_PROJECT]   Will setDocument:', docRes?.data?.id || 'null');
      
      setProject(projectRes.data);
      setDocument(docRes?.data || null);
      setError('');
      
      // Restore active tab after loading (if it was preserved)
      if (preservedTab && preservedTab !== activeTab) {
        console.log('[LOAD_PROJECT] Restoring active tab to:', preservedTab);
        setActiveTab(preservedTab);
      }
      
      console.log('[LOAD_PROJECT] State updated successfully');
      console.log('[LOAD_PROJECT] ============================================');
    } catch (err) {
      const errorMsg = err.extractedMessage || err.response?.data?.detail || err.message || 'Failed to load project';
      setError(typeof errorMsg === 'string' ? errorMsg : 'Failed to load project');
      console.error('[LOAD_PROJECT] Error:', err);
    } finally {
      if (!isRefreshing) {
        setLoading(false);
      }
    }
  };

  const handleExport = async (type = 'auto') => {
    try {
      setExportLoading(true);
      let response;
      if (type === 'docx') {
        response = await exportAPI.exportWord(id);
      } else if (type === 'pptx') {
        response = await exportAPI.exportPowerPoint(id);
      } else {
        response = await exportAPI.exportDocument(id);
      }

      // Check if response is valid
      if (!response || !response.data) {
        throw new Error('Invalid response from server');
      }

      // Get filename from Content-Disposition header
      const contentDisposition = response.headers['content-disposition'] || response.headers['Content-Disposition'];
      let filename = `document.${project.document_type === 'word' ? 'docx' : 'pptx'}`;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/['"]/g, '');
        }
      }

      // For blob responses, response.data is already a Blob
      const blob = response.data instanceof Blob 
        ? response.data 
        : new Blob([response.data], {
            type: response.headers['content-type'] || response.headers['Content-Type'] || 'application/octet-stream',
          });

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = window.document.createElement('a');
      a.href = url;
      a.download = filename;
      window.document.body.appendChild(a);
      a.click();
      
      // Cleanup
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
        window.document.body.removeChild(a);
        setExportLoading(false);
      }, 100);
    } catch (err) {
      setExportLoading(false);
      let errorMsg = err.extractedMessage || err.response?.data?.detail || err.message || 'Failed to export document';
      
      // Handle empty objects or arrays
      if (typeof errorMsg === 'object') {
        if (Array.isArray(errorMsg)) {
          errorMsg = errorMsg.map(e => typeof e === 'string' ? e : e.msg || JSON.stringify(e)).join(', ');
        } else if (Object.keys(errorMsg).length === 0) {
          errorMsg = 'An unknown error occurred during export. Please check the console for details.';
        } else {
          errorMsg = JSON.stringify(errorMsg);
        }
      }
      
      // Ensure it's a string
      const displayMsg = typeof errorMsg === 'string' && errorMsg.trim() 
        ? errorMsg.trim() 
        : 'Failed to export document. Please try again.';
      
      alert(`Failed to export document: ${displayMsg}`);
      console.error('Export error:', err);
    }
  };

  // CRITICAL: Only show loading screen on initial load, not on refresh
  // This prevents RefinementInterface from unmounting during refresh
  if (loading && !project) {
    console.log('[PROJECT_DETAIL] Showing loading screen (initial load)');
    return (
      <div className="project-detail-container">
        <div className="container">
          <div className="loading">
            <div className="spinner"></div>
            <p style={{ marginTop: '16px', color: 'var(--text-secondary)' }}>Loading project...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="project-detail-container">
        <div className="container">
          <div className="card" style={{ textAlign: 'center', padding: 'var(--spacing-3xl)' }}>
            <div className="error" style={{ marginBottom: 'var(--spacing-lg)' }}>
              {error || 'Project not found'}
            </div>
            <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="project-detail-container">
      <div className="container">
        {/* Hero Header Section */}
        <div className="project-hero-header">
          <div className="project-hero-content">
            <div className="project-hero-left">
              <h1 className="project-hero-title">{project.title || project.main_topic}</h1>
            </div>
            {document && document.content && (
              <div className="project-hero-actions">
                <button
                  className="btn-export-premium"
                  onClick={() => handleExport()}
                  disabled={exportLoading}
                >
                  {exportLoading ? (
                    <>
                      <div className="spinner spinner-small"></div>
                      <span>Exporting</span>
                    </>
                  ) : (
                    <>
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="7 10 12 15 17 10" />
                        <line x1="12" y1="15" x2="12" y2="3" />
                      </svg>
                      <span>Export {project.document_type === 'word' ? '.docx' : '.pptx'}</span>
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Step Navigation - Dashboard Style */}
        <div className="step-navigation">
          <button
            className={`step-nav-item ${activeTab === 'configure' ? 'active' : ''}`}
            onClick={() => setActiveTab('configure')}
          >
            Configure
          </button>
          <button
            className={`step-nav-item ${activeTab === 'generate' ? 'active' : ''}`}
            onClick={() => setActiveTab('generate')}
            disabled={!document}
          >
            Generate
          </button>
          <button
            className={`step-nav-item ${activeTab === 'refine' ? 'active' : ''}`}
            onClick={() => setActiveTab('refine')}
            disabled={!document || !document.content}
          >
            Refine
          </button>
        </div>

        {/* Main Content Area */}
        <div className="main-content-area">
          <div className="tab-content">
            {activeTab === 'configure' && (
              <DocumentConfiguration
                project={project}
                document={document}
                onUpdate={loadProject}
              />
            )}
            {activeTab === 'generate' && (
              <ContentGeneration
                project={project}
                document={document}
                onUpdate={loadProject}
              />
            )}
            {activeTab === 'refine' && (
              <RefinementInterface
                key={`refine-${project.id}`}
                project={project}
                document={document}
                onUpdate={loadProject}
              />
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default ProjectDetail;
