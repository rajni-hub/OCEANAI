import { useState } from 'react';
import { generationAPI } from '../services/api';
import './ContentGeneration.css';

const ContentGeneration = ({ project, document, onUpdate }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [content, setContent] = useState(document?.content || {});

  const handleGenerate = async () => {
    if (!document) {
      setError('Please configure the document structure first');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await generationAPI.generateContent(project.id);
      setContent(response.data.content || {});
      setSuccess('Content generated.');
      onUpdate();
    } catch (err) {
      const errorMsg = err.extractedMessage || err.response?.data?.detail || err.message || 'Failed to generate content';
      setError(typeof errorMsg === 'string' ? errorMsg : 'Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  const items = project.document_type === 'word'
    ? (document?.structure?.sections || [])
    : (document?.structure?.slides || []);
  const itemType = project.document_type === 'word' ? 'section' : 'slide';

  return (
    <div className="content-generation">
      <div className="generation-header">
        <h2>Generate Content</h2>
        <button
          className="btn btn-primary"
          onClick={handleGenerate}
          disabled={loading || !document}
        >
          {loading ? 'Generating' : 'Generate'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {!document ? (
        <div className="info-message">
          Please configure the document structure first before generating content.
        </div>
      ) : (
        <div className="content-preview">
          {items.length === 0 ? (
            <div className="info-message">
              No {itemType}s configured. Please add {itemType}s in the Configure tab.
            </div>
          ) : (
            items.map((item) => (
              <div key={item.id} className="content-item">
                <h3>{item.title}</h3>
                <div className="content-text">
                  {content[item.id] ? (
                    <pre>{content[item.id]}</pre>
                  ) : (
                    <p className="no-content">Content not generated yet</p>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default ContentGeneration;

