import { useState, useEffect, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  // Slider state
  const [currentSlide, setCurrentSlide] = useState(0);
  const sliderIntervalRef = useRef(null);

  // Slide content data - Product-focused messaging with unique illustrations (same as Login)
  const slides = [
    {
      tagline: "AI-Powered Document Creation - Generate professional Word documents and PowerPoint presentations with intelligent content generation",
      illustration: (
        <svg width="120" height="120" viewBox="0 0 120 120" fill="none" className="auth-illustration">
          {/* AI Document Creation - Document with sparkles */}
          <rect x="30" y="25" width="60" height="70" rx="4" fill="currentColor" fillOpacity="0.15" stroke="currentColor" strokeWidth="2" strokeOpacity="0.3"/>
          <line x1="40" y1="40" x2="80" y2="40" stroke="currentColor" strokeWidth="2" strokeOpacity="0.4"/>
          <line x1="40" y1="55" x2="75" y2="55" stroke="currentColor" strokeWidth="2" strokeOpacity="0.4"/>
          <line x1="40" y1="70" x2="70" y2="70" stroke="currentColor" strokeWidth="2" strokeOpacity="0.4"/>
          {/* AI Sparkles */}
          <circle cx="85" cy="30" r="3" fill="currentColor" fillOpacity="0.6"/>
          <circle cx="90" cy="35" r="2" fill="currentColor" fillOpacity="0.5"/>
          <circle cx="25" cy="40" r="2.5" fill="currentColor" fillOpacity="0.5"/>
          <path d="M85 25 L88 28 M88 25 L85 28" stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.6"/>
        </svg>
      )
    },
    {
      tagline: "Smart Refinement & Workflow Automation - Refine content section by section with AI assistance and streamline your document workflow",
      illustration: (
        <svg width="120" height="120" viewBox="0 0 120 120" fill="none" className="auth-illustration">
          {/* Smart Refinement - Gear/Automation icon */}
          <circle cx="60" cy="60" r="30" fill="none" stroke="currentColor" strokeWidth="2.5" strokeOpacity="0.3"/>
          <circle cx="60" cy="60" r="20" fill="none" stroke="currentColor" strokeWidth="2" strokeOpacity="0.4"/>
          {/* Gear teeth */}
          <rect x="55" y="25" width="10" height="8" rx="2" fill="currentColor" fillOpacity="0.4"/>
          <rect x="55" y="87" width="10" height="8" rx="2" fill="currentColor" fillOpacity="0.4"/>
          <rect x="25" y="55" width="8" height="10" rx="2" fill="currentColor" fillOpacity="0.4"/>
          <rect x="87" y="55" width="8" height="10" rx="2" fill="currentColor" fillOpacity="0.4"/>
          {/* Refinement arrows */}
          <path d="M35 60 L45 55 L45 65 Z" fill="currentColor" fillOpacity="0.5"/>
          <path d="M85 60 L75 55 L75 65 Z" fill="currentColor" fillOpacity="0.5"/>
          <circle cx="60" cy="60" r="8" fill="currentColor" fillOpacity="0.3"/>
        </svg>
      )
    },
    {
      tagline: "Professional Results with Minimal Effort - Export polished .docx and .pptx files that meet the highest quality standards effortlessly",
      illustration: (
        <svg width="120" height="120" viewBox="0 0 120 120" fill="none" className="auth-illustration">
          {/* Professional Output - Checkmark with document */}
          <rect x="35" y="30" width="50" height="60" rx="3" fill="currentColor" fillOpacity="0.15" stroke="currentColor" strokeWidth="2" strokeOpacity="0.3"/>
          <line x1="45" y1="45" x2="70" y2="45" stroke="currentColor" strokeWidth="2" strokeOpacity="0.3"/>
          <line x1="45" y1="60" x2="65" y2="60" stroke="currentColor" strokeWidth="2" strokeOpacity="0.3"/>
          {/* Success checkmark */}
          <path d="M50 75 L58 83 L75 66" stroke="currentColor" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeOpacity="0.6"/>
          {/* Quality stars */}
          <path d="M25 50 L26.5 53 L30 53.5 L27.5 56 L28 59.5 L25 57.5 L22 59.5 L22.5 56 L20 53.5 L23.5 53 Z" fill="currentColor" fillOpacity="0.5"/>
          <path d="M95 50 L96.5 53 L100 53.5 L97.5 56 L98 59.5 L95 57.5 L92 59.5 L92.5 56 L90 53.5 L93.5 53 Z" fill="currentColor" fillOpacity="0.5"/>
        </svg>
      )
    }
  ];

  // Auto-advance slider every 5 seconds
  useEffect(() => {
    sliderIntervalRef.current = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);

    return () => {
      if (sliderIntervalRef.current) {
        clearInterval(sliderIntervalRef.current);
      }
    };
  }, [slides.length]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    const result = await register(email, password);
    
    if (result.success) {
      setSuccess('Registration successful. Redirecting...');
      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } else {
      const errorMsg = result.error || 'Registration failed';
      setError(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
    }
    
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="auth-two-panel">
        {/* Left Panel - Branding & Illustration with Slider */}
        <div className="auth-left-panel">
          <div className="auth-slider-container">
            <div className="auth-slider-track">
              {slides.map((slide, index) => (
                <div 
                  key={index} 
                  className={`auth-slide ${currentSlide === index ? 'active' : ''}`}
                >
                  <div className="auth-brand-panel">
                    <div className="auth-illustration-area">
                      <div className="auth-illustration-circle">
                        {slide.illustration}
                      </div>
                    </div>
                    <h1 className="auth-brand-title">OCEAN AI</h1>
                    <p className="auth-brand-tagline">
                      {slide.tagline}
                    </p>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Dot Indicators */}
            <div className="auth-slider-dots">
              {slides.map((_, index) => (
                <button
                  key={index}
                  className={`auth-slider-dot ${currentSlide === index ? 'active' : ''}`}
                  onClick={() => {
                    setCurrentSlide(index);
                    // Reset timer on manual click
                    if (sliderIntervalRef.current) {
                      clearInterval(sliderIntervalRef.current);
                    }
                    sliderIntervalRef.current = setInterval(() => {
                      setCurrentSlide((prev) => (prev + 1) % slides.length);
                    }, 5000);
                  }}
                  aria-label={`Go to slide ${index + 1}`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Right Panel - Registration Form */}
        <div className="auth-right-panel">
          <div className="auth-form-wrapper">
            <div className="auth-form-logo">
              <div className="auth-form-logo-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor"/>
                  <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" fill="none"/>
                  <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" fill="none"/>
                </svg>
              </div>
              <span className="auth-form-logo-text">
                <span className="auth-form-logo-text-main">OCEAN</span>
                <span className="auth-form-logo-text-accent">AI</span>
              </span>
            </div>

            <div className="auth-card">
              <div className="auth-card-header">
                <h2>Create account</h2>
                <p>Get started with document authoring</p>
              </div>
              
              <form onSubmit={handleSubmit} className="auth-form">
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="you@example.com"
                    className="auth-input"
                  />
                </div>
                
                <div className="form-group">
                  <label>Password</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="Minimum 6 characters"
                    className="auth-input"
                  />
                </div>
                
                <div className="form-group">
                  <label>Confirm Password</label>
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    placeholder="Re-enter your password"
                    className="auth-input"
                  />
                </div>
                
                {error && <div className="error">{error}</div>}
                {success && <div className="success">{success}</div>}
                
                <button 
                  type="submit" 
                  className="btn btn-primary auth-submit" 
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <div className="spinner spinner-small"></div>
                      <span>Creating account</span>
                    </>
                  ) : (
                    'Create account'
                  )}
                </button>
              </form>
              
              <div className="auth-divider">
                <span className="auth-divider-line"></span>
                <span className="auth-divider-text">or</span>
                <span className="auth-divider-line"></span>
              </div>

              <div className="auth-footer">
                <p>
                  Already have an account?{' '}
                  <Link to="/login" className="auth-link">
                    Sign in
                  </Link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
