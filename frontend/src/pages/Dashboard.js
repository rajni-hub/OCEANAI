import { useState, useEffect, useRef } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { projectsAPI } from "../services/api";
import "./Dashboard.css";

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const carouselRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [scrollLeft, setScrollLeft] = useState(0);
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    loadProjects();
    // Reset exit state when component mounts (coming back from another page)
    setIsExiting(false);
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const response = await projectsAPI.getProjects();
      setProjects(response.data.projects || []);
      setError("");
    } catch (err) {
      const errorMsg =
        err.extractedMessage ||
        err.response?.data?.detail ||
        err.message ||
        "Failed to load projects";
      setError(
        typeof errorMsg === "string" ? errorMsg : JSON.stringify(errorMsg)
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (window.confirm("Delete this project?")) {
      try {
        await projectsAPI.deleteProject(id);
        loadProjects();
      } catch (err) {
        alert("Failed to delete project");
      }
    }
  };

  // Carousel navigation
  const scrollCarousel = (direction) => {
    if (carouselRef.current) {
      const scrollAmount = 400;
      carouselRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  // Touch/swipe handlers for mobile
  const handleMouseDown = (e) => {
    setIsDragging(true);
    setStartX(e.pageX - carouselRef.current.offsetLeft);
    setScrollLeft(carouselRef.current.scrollLeft);
  };

  const handleMouseLeave = () => {
    setIsDragging(false);
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - carouselRef.current.offsetLeft;
    const walk = (x - startX) * 2;
    carouselRef.current.scrollLeft = scrollLeft - walk;
  };

  // Touch handlers
  const handleTouchStart = (e) => {
    setIsDragging(true);
    setStartX(e.touches[0].pageX - carouselRef.current.offsetLeft);
    setScrollLeft(carouselRef.current.scrollLeft);
  };

  const handleTouchMove = (e) => {
    if (!isDragging) return;
    const x = e.touches[0].pageX - carouselRef.current.offsetLeft;
    const walk = (x - startX) * 2;
    carouselRef.current.scrollLeft = scrollLeft - walk;
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="container">
          <div className="loading">
            <div className="spinner"></div>
          </div>
        </div>
      </div>
    );
  }

  // Handle navigation with smooth transition
  const handleCreateNow = (e) => {
    e.preventDefault();
    setIsExiting(true);
    setTimeout(() => {
      navigate("/projects/new");
    }, 300); // Half of animation duration for smoother feel
  };

  return (
    <div className={`dashboard-container ${isExiting ? "exiting" : ""}`}>
      <div className="container">
        {/* Hero Section - Bold "CREATE SMART DOCUMENTS" Style */}
        <div className="dashboard-hero">
          <div className="hero-content">
            <div className="hero-text">
              <p className="hero-tagline">
                Generate professional .docx and .pptx files instantly with AI
                assistance.
              </p>
              <h1 className="hero-heading">
                <span className="hero-line hero-line-create">CREATE</span>
                <span className="hero-line hero-line-smart">SMART</span>
                <span className="hero-line hero-line-right">DOCUMENTS</span>
              </h1>
              <div className="hero-scroll-indicator">
                <p className="scroll-hint">Scroll to view your projects</p>
                <button
                  className="scroll-arrow"
                  onClick={() => {
                    const projectsSection =
                      document.querySelector(".projects-section");
                    if (projectsSection) {
                      projectsSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start",
                      });
                    }
                  }}
                  aria-label="Scroll to projects"
                >
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M6 9l6 6 6-6" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="hero-cta-wrapper">
              <button
                onClick={handleCreateNow}
                className="btn btn-hero btn-hero-primary"
              >
                <span className="btn-text">CREATE NOW</span>
                <span className="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>

        {error && <div className="error">{error}</div>}

        {projects.length === 0 ? (
          <div className="empty-state">
            <h2>Start Your First Project</h2>
            <p>
              Create professional Word documents and PowerPoint presentations
              with AI assistance.
            </p>
            <button
              onClick={handleCreateNow}
              className="btn btn-primary btn-large"
            >
              Create Project
            </button>
          </div>
        ) : (
          <div className="projects-section">
            <div className="section-header">
              <h2 className="section-title">YOUR PROJECTS</h2>
            </div>
            <div className="carousel-container">
              {/* Left Bouncy Arrow */}
              <button
                className="carousel-arrow carousel-arrow-left"
                onClick={() => {
                  const carousel = carouselRef.current;
                  if (carousel) {
                    carousel.scrollBy({ left: -400, behavior: "smooth" });
                  }
                }}
                aria-label="Scroll left"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M15 18l-6-6 6-6" />
                </svg>
              </button>

              <div
                className="projects-carousel"
                ref={carouselRef}
                onMouseDown={handleMouseDown}
                onMouseLeave={handleMouseLeave}
                onMouseUp={handleMouseUp}
                onMouseMove={handleMouseMove}
                onTouchStart={handleTouchStart}
                onTouchMove={handleTouchMove}
                onTouchEnd={handleTouchEnd}
              >
                {projects.map((project, index) => (
                  <div key={project.id} className="project-card">
                    {/* Floating Badge */}
                    {index === 0 && (
                      <div className="project-badge">NEW PROJECT</div>
                    )}

                    {/* Image Area */}
                    <div className="project-card-image">
                      <div className="project-image-placeholder">
                        {project.document_type === "word" ? (
                          <svg
                            width="80"
                            height="80"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.5"
                          >
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <polyline points="10 9 9 9 8 9"></polyline>
                          </svg>
                        ) : (
                          <svg
                            width="80"
                            height="80"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.5"
                          >
                            <rect
                              x="3"
                              y="3"
                              width="18"
                              height="18"
                              rx="2"
                              ry="2"
                            ></rect>
                            <line x1="9" y1="3" x2="9" y2="21"></line>
                            <line x1="3" y1="9" x2="21" y2="9"></line>
                          </svg>
                        )}
                      </div>
                    </div>

                    {/* Content Area */}
                    <div className="project-card-content">
                      <div className="project-type-tag">
                        {project.document_type.toUpperCase()}
                      </div>
                      <h3 className="project-title">{project.main_topic}</h3>
                      <p className="project-description">{project.title}</p>
                      <div className="project-date">
                        {new Date(project.created_at).toLocaleDateString(
                          "en-US",
                          {
                            month: "short",
                            day: "numeric",
                            year: "numeric",
                          }
                        )}
                      </div>
                      <button
                        className="project-cta-btn"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/projects/${project.id}`);
                        }}
                      >
                        VIEW PROJECT →
                      </button>
                      <button
                        className="project-delete-btn"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(project.id, e);
                        }}
                        aria-label="Delete project"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Right Bouncy Arrow */}
              <button
                className="carousel-arrow carousel-arrow-right"
                onClick={() => {
                  const carousel = carouselRef.current;
                  if (carousel) {
                    carousel.scrollBy({ left: 400, behavior: "smooth" });
                  }
                }}
                aria-label="Scroll right"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M9 18l6-6-6-6" />
                </svg>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
