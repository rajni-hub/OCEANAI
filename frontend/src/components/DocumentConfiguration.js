import { useState, useEffect } from 'react';
import { documentsAPI } from '../services/api';
import './DocumentConfiguration.css';

const DocumentConfiguration = ({ project, document, onUpdate }) => {
  const [sections, setSections] = useState([]);
  const [slides, setSlides] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [newSectionTitle, setNewSectionTitle] = useState('');
  const [newSlideTitle, setNewSlideTitle] = useState('');

  useEffect(() => {
    if (document) {
      if (project.document_type === 'word') {
        setSections(document.structure?.sections || []);
      } else {
        setSlides(document.structure?.slides || []);
      }
    }
  }, [document, project]);

  const handleAddSection = () => {
    if (!newSectionTitle.trim()) return;
    
    const newSection = {
      id: `section-${Date.now()}`,
      title: newSectionTitle.trim(),
      order: sections.length,
    };
    
    setSections([...sections, newSection]);
    setNewSectionTitle('');
  };

  const handleAddSlide = () => {
    if (!newSlideTitle.trim()) return;
    
    const newSlide = {
      id: `slide-${Date.now()}`,
      title: newSlideTitle.trim(),
      order: slides.length,
    };
    
    setSlides([...slides, newSlide]);
    setNewSlideTitle('');
  };

  const handleRemove = (id) => {
    if (project.document_type === 'word') {
      setSections(sections.filter(s => s.id !== id));
    } else {
      setSlides(slides.filter(s => s.id !== id));
    }
  };

  const handleReorder = (id, direction) => {
    if (project.document_type === 'word') {
      const index = sections.findIndex(s => s.id === id);
      if (index === -1) return;
      
      const newIndex = direction === 'up' ? index - 1 : index + 1;
      if (newIndex < 0 || newIndex >= sections.length) return;
      
      const newSections = [...sections];
      [newSections[index], newSections[newIndex]] = [newSections[newIndex], newSections[index]];
      newSections[index].order = index;
      newSections[newIndex].order = newIndex;
      setSections(newSections);
    } else {
      const index = slides.findIndex(s => s.id === id);
      if (index === -1) return;
      
      const newIndex = direction === 'up' ? index - 1 : index + 1;
      if (newIndex < 0 || newIndex >= slides.length) return;
      
      const newSlides = [...slides];
      [newSlides[index], newSlides[newIndex]] = [newSlides[newIndex], newSlides[index]];
      newSlides[index].order = index;
      newSlides[newIndex].order = newIndex;
      setSlides(newSlides);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const structure = project.document_type === 'word'
        ? { structure: { sections } }
        : { structure: { slides } };

      if (document) {
        await documentsAPI.updateDocumentStructure(project.id, structure);
      } else {
        await documentsAPI.configureDocument(project.id, structure);
      }
      
      setSuccess('Configuration saved.');
      onUpdate();
    } catch (err) {
      const errorMsg = err.extractedMessage || err.response?.data?.detail || err.message || 'Failed to save configuration';
      setError(typeof errorMsg === 'string' ? errorMsg : 'Failed to save configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleAISuggest = async () => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await documentsAPI.aiSuggestTemplate(
        project.id,
        project.document_type,
        project.main_topic
      );
      
      // Response has structure.sections or structure.slides
      const structure = response.data.structure || {};
      if (project.document_type === 'word') {
        setSections(structure.sections || []);
      } else {
        setSlides(structure.slides || []);
      }
      
      setSuccess('Template generated. Review and save.');
    } catch (err) {
      const errorMsg = err.extractedMessage || err.response?.data?.detail || err.message || 'Failed to generate AI template';
      setError(typeof errorMsg === 'string' ? errorMsg : 'Failed to generate AI template');
    } finally {
      setLoading(false);
    }
  };

  const items = project.document_type === 'word' ? sections : slides;
  const setItems = project.document_type === 'word' ? setSections : setSlides;
  const newTitle = project.document_type === 'word' ? newSectionTitle : newSlideTitle;
  const setNewTitle = project.document_type === 'word' ? setNewSectionTitle : setNewSlideTitle;
  const handleAdd = project.document_type === 'word' ? handleAddSection : handleAddSlide;
  const itemType = project.document_type === 'word' ? 'section' : 'slide';

  return (
    <div className="document-configuration">
      <div className="config-header">
        <h2>Configure {project.document_type === 'word' ? 'Sections' : 'Slides'}</h2>
        <button
          className="btn-ai-suggest"
          onClick={handleAISuggest}
          disabled={loading}
        >
          AI suggest
        </button>
      </div>

      <div className="add-item-form">
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder={`Add new ${itemType} title...`}
          onKeyPress={(e) => e.key === 'Enter' && handleAdd()}
        />
        <button className="btn-add" onClick={handleAdd}>
          Add
        </button>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="items-list">
        {items.length === 0 ? (
          <p className="empty-message">No {itemType}s yet. Add one above.</p>
        ) : (
          items.map((item, index) => (
            <div key={item.id} className="item-card">
              <div className="item-content">
                <span className="item-number">{index + 1}</span>
                <span className="item-title">{item.title}</span>
              </div>
              <div className="item-actions">
                <button
                  className="btn btn-reorder"
                  onClick={() => handleReorder(item.id, 'up')}
                  disabled={index === 0}
                  aria-label="Move up"
                >
                  ↑
                </button>
                <button
                  className="btn btn-reorder"
                  onClick={() => handleReorder(item.id, 'down')}
                  disabled={index === items.length - 1}
                  aria-label="Move down"
                >
                  ↓
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => handleRemove(item.id)}
                  aria-label="Remove"
                >
                  Remove
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="config-actions">
        <button
          className="btn btn-primary"
          onClick={handleSave}
          disabled={loading || items.length === 0}
        >
          {loading ? 'Saving' : 'Save'}
        </button>
      </div>
    </div>
  );
};

export default DocumentConfiguration;

